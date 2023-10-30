import dataclasses
import json
import pathlib
import re
import typing

import yaml

from whocan import _errors
from whocan import _environment

DEFAULT_ENV = _environment.PolicyEnvironment({})


def _force_to_list(value: typing.Union[typing.List[str], str]) -> typing.List[str]:
    """Force the value to a list."""
    if isinstance(value, str):
        return [value]
    return value


def _policy_check(raise_issue: bool, message: str):
    """Raise the error if raise_issue is true."""
    if raise_issue:
        raise _errors.PolicyYamlInvalidError(message)


def _validate_yaml(raw_yaml: typing.Any):
    """Validate the yaml or raise an error if it is invalid."""
    if not isinstance(raw_yaml, dict):
        raise _errors.PolicyYamlInvalidError(
            "Top level of policy must be a dictionary."
        )
    _policy_check("statements" not in raw_yaml, 'Missing required field "statements".')
    _policy_check(
        not isinstance(raw_yaml["statements"], list), '"statements" must be a list.'
    )

    for i, statement in enumerate(raw_yaml["statements"]):
        required = ["effect", "actions"]
        for r in required:
            _policy_check(
                r not in statement, f'Missing required field "statements[{i}].{r}".'
            )
        _policy_check(
            not ("principals" in statement or "resources" in statement),
            (
                f'Missing required field in "statements[{i}]". Must include '
                'either "resources" or "principals".'
            ),
        )
        _policy_check(
            statement["effect"] not in {"allow", "deny"},
            f'Missing required field "statements[{i}].effect"'
            ' must be "allow" or "deny".',
        )
        _policy_check(
            (
                "resources" in statement
                and not isinstance(statement["resources"], (str, list))
            ),
            f'"statements[{i}].resources" must be a string or list.',
        )
        _policy_check(
            (
                "principals" in statement
                and not isinstance(statement["principals"], (str, list))
            ),
            f'"statements[{i}].principals" must be a string or list.',
        )
        _policy_check(
            not isinstance(statement["actions"], (str, list)),
            f'Missing required field "statements[{i}].actions"'
            " must be a string or list.",
        )
        key = "resources"
        if key in statement and isinstance(statement[key], list):
            _policy_check(
                any(not isinstance(r, str) for r in statement["resources"]),
                f'All members of "statements[{i}].resources" must be strings.',
            )
        key = "principals"
        if key in statement and isinstance(statement[key], list):
            _policy_check(
                any(not isinstance(r, str) for r in statement["principals"]),
                f'All members of "statements[{i}].principals" must be strings.',
            )
        if isinstance(statement["actions"], list):
            _policy_check(
                any(not isinstance(a, str) for a in statement["actions"]),
                f'All members of "statements[{i}].actions" must be strings.',
            )


def _form_regex(
    base: str,
    arguments: typing.Dict[str, str],
    strict: bool,
) -> str:
    """Form a regex from the given base value and arguments."""
    previous = 0
    processed = []
    for m in re.finditer(r"((?:\${\s*(\w+)\s*})|\*+)", base):
        if m.start() != previous:
            processed.append(re.escape(base[previous : m.start()]))
        if m.group(1) == "*":
            processed.append("[^/]*")
        if m.group(1).startswith("**"):
            processed.append(".*")
        if m.group(2):
            parameter = m.group(2)
            if parameter not in arguments and strict:
                raise _errors.PolicyEvaluationError(f'"{parameter}" unknown variable.')
            processed.append(str(arguments.get(parameter, "")))
        previous = m.end()
    processed.append(re.escape(base[previous:]))
    pattern = "".join(processed)
    return f"^{pattern}$"


@dataclasses.dataclass
class ConditionsDetailedEvaluation:
    """The evaluation of a condition."""

    key: str
    operator: str
    argument_value: typing.Any
    condition_value: typing.Any
    result: bool


@dataclasses.dataclass
class ConditionsResult:
    """The result of evaluating all conditions."""

    result: bool
    condition_results: typing.List[ConditionsDetailedEvaluation]


def _conditions_meet(
    env: _environment.PolicyEnvironment,
    conditions: typing.Optional[typing.List["Condition"]],
    arguments: typing.Dict[str, str],
) -> ConditionsResult:
    """Determine if the conditions have been meet."""
    evaluations = [
        ConditionsDetailedEvaluation(
            c.key,
            c.operator,
            arguments.get(c.key),
            c.value,
            env.condition_functions[c.operator](arguments.get(c.key), c.value),
        )
        for c in conditions or []
    ]
    return ConditionsResult(all(e.result for e in evaluations), evaluations)


@dataclasses.dataclass
class Condition:
    """A condition of the statement."""

    operator: str
    key: str
    value: typing.Any


@dataclasses.dataclass
class Line:
    """A single resource or action."""

    raw_line: str
    arguments: typing.Dict[str, str]
    strict: bool = True

    def is_match(self, value: str) -> bool:
        """Determine if the given value is a match for the line."""
        if self.line == "*":
            return True
        values = value.split(":")
        pieces = self.line.split(":")
        if len(values) != len(pieces):
            return False
        for piece, incoming in zip(pieces, values):
            pattern = _form_regex(piece, self.arguments, self.strict)
            if not re.fullmatch(pattern, incoming):
                return False
        return True

    @property
    def line(self) -> str:
        """Get the line with arguments rendered in."""
        previous = 0
        processed = []
        for m in re.finditer(r"((?:\${\s*(\w+)\s*}))", self.raw_line):
            if m.start() != previous:
                processed.append(self.raw_line[previous : m.start()])
            if m.group(2):
                parameter = m.group(2)
                if parameter not in self.arguments and self.strict:
                    raise _errors.PolicyEvaluationError(
                        f'"{parameter}" unknown variable.'
                    )
                processed.append(str(self.arguments.get(parameter, "")))
            previous = m.end()
        processed.append(self.raw_line[previous:])
        return "".join(processed)


@dataclasses.dataclass
class StatementDetailedEvaluation:
    """The evaluation of a statement."""

    result: typing.Optional[str]
    matched_actions: typing.List[str]
    matched_resources: typing.List[str]
    matched_principals: typing.List[str]
    condition_results: ConditionsResult
    statement: "Statement"


@dataclasses.dataclass
class Statement:
    """A singular set of actions and resources."""

    effect: str
    actions: typing.List[str]
    resources: typing.Optional[typing.List[str]] = None
    principals: typing.Optional[typing.List[str]] = None
    conditions: typing.Optional[typing.List[Condition]] = None

    def evaluate(
        self,
        action: str,
        resource: typing.Optional[str] = None,
        principal: typing.Optional[str] = None,
        arguments: typing.Dict[str, str] = None,
        env: _environment.PolicyEnvironment = DEFAULT_ENV,
    ) -> typing.Optional[str]:
        """
        Evaluate the statement to determine if it allows, denys, or has no
        effect on the specified resource and action.

        :param action:
            The action being taken on the specified resource.
        :param resource:
            The resource on which the action is being taken.
        :param principal:
            The principal who desires to take the action.
        :param arguments:
            Arguments to pass into the policy before determining if
            access is allowed.
        :return:
            Either "allow", "deny" or None.
        """
        return self.debug(action, resource, principal, arguments, env).result

    def debug(
        self,
        action: str,
        resource: typing.Optional[str] = None,
        principal: typing.Optional[str] = None,
        arguments: typing.Dict[str, str] = None,
        env: _environment.PolicyEnvironment = DEFAULT_ENV,
    ) -> StatementDetailedEvaluation:
        """
        Debug the statement to determine why it allows, denys, or has no
        effect on the specified resource and action.

        :param action:
            The action being taken on the specified resource.
        :param resource:
            The resource on which the action is being taken.
        :param principal:
            The principal who desires to take the action.
        :param arguments:
            Arguments to pass into the policy before determining if
            access is allowed.
        :return:
            A detailed evaluation of the statement.
        """
        arguments = arguments if arguments else {}
        checks = [
            ("actions", action, self.actions),
            ("resources", resource, self.resources),
            ("principals", principal, self.principals),
        ]
        details = {}
        results = []
        for field, incoming, lines in checks:
            details[f"matched_{field}"] = []
            if incoming is None and lines is None:
                results.append(True)
                continue
            if incoming is None or lines is None:
                results.append(False)
                continue
            for l in lines:
                line = Line(l, arguments)
                if line.is_match(incoming):
                    details[f"matched_{field}"].append(line.line)
            results.append(len(details[f"matched_{field}"]) > 0)
        conditions_meet = _conditions_meet(env, self.conditions, arguments)
        result = self.effect if all(results) and conditions_meet.result else None
        return StatementDetailedEvaluation(
            result,
            details["matched_actions"],
            details["matched_resources"],
            details["matched_principals"],
            conditions_meet,
            self,
        )

    def to_jsonable(self) -> dict:
        """Serialize the statement to a JSONable object."""
        resources = [r for r in self.resources] if self.resources is not None else None
        principals = (
            [r for r in self.principals] if self.principals is not None else None
        )
        conditions = (
            [dataclasses.asdict(c) for c in self.conditions]
            if self.conditions is not None
            else None
        )
        base = {
            "effect": self.effect,
            "actions": self.actions,
            "resources": resources,
            "principals": principals,
            "conditions": conditions,
        }
        return {k: v for k, v in base.items() if v is not None}

    @classmethod
    def from_jsonable(cls, jsonable: dict) -> dict:
        """Deserialize the policy set from a JSONable object."""
        conditions = [
            Condition(c["operator"], c["key"], c["value"])
            for c in _force_to_list(jsonable.get("conditions")) or []
        ]
        return cls(
            jsonable["effect"],
            _force_to_list(jsonable["actions"]),
            _force_to_list(jsonable.get("resources")),
            _force_to_list(jsonable.get("principals")),
            conditions if jsonable.get("conditions") is not None else None,
        )


@dataclasses.dataclass
class PolicyDetailedEvaluation:
    """The evaluation of a policy."""

    result: typing.Optional[str]
    statement_evaluations: typing.List[StatementDetailedEvaluation]

    def __str__(self):
        """Get a string representation of the evaluation."""
        return json.dumps(dataclasses.asdict(self), indent=2)


@dataclasses.dataclass
class Policy:
    """An policy defining resource access."""

    statements: typing.List[Statement]

    def is_allowed(
        self,
        action: str,
        resource: str = None,
        principal: str = None,
        arguments: typing.Dict[str, str] = None,
        env: _environment.PolicyEnvironment = DEFAULT_ENV,
    ) -> bool:
        """
        Determine if the given policy allows the specified action on the
        specified resource.

        :param action:
            The action being taken on the specified resource.
        :param resource:
            The resource on which the action is being taken.
        :param arguments:
            Arguments to pass into the policy before determining if
            access is allowed.
        :return:
            Whether the action is allowed on the resource.
        """
        result = self.evaluate(action, resource, principal, arguments, env)
        return "allow" == result

    def evaluate(
        self,
        action: str,
        resource: str = None,
        principal: str = None,
        arguments: typing.Dict[str, str] = None,
        env: _environment.PolicyEnvironment = DEFAULT_ENV,
    ) -> typing.Optional[str]:
        """
        Evaluate the policy to determine if it allows, denys, or makes no
        comment on the specified resource and action.

        :param action:
            The action being taken on the specified resource.
        :param resource:
            The resource on which the action is being taken.
        :param arguments:
            Arguments to pass into the policy before determining if
            access is allowed.
        :return:
            Either "allow", "deny" or None.
        """
        return self.debug(action, resource, principal, arguments, env).result

    def debug(
        self,
        action: str,
        resource: str = None,
        principal: str = None,
        arguments: typing.Dict[str, str] = None,
        env: _environment.PolicyEnvironment = DEFAULT_ENV,
    ) -> PolicyDetailedEvaluation:
        """
        Evaluate the policy to determine why it allows, denys, or makes no
        comment on the specified resource and action.

        :param action:
            The action being taken on the specified resource.
        :param resource:
            The resource on which the action is being taken.
        :param arguments:
            Arguments to pass into the policy before determining if
            access is allowed.
        :return:
            A detailed evaluation of the policy.
        """
        evaluations = [
            statement.debug(action, resource, principal, arguments, env)
            for statement in self.statements
        ]
        result = None
        if any(v.result == "allow" for v in evaluations):
            result = "allow"
        if any(v.result == "deny" for v in evaluations):
            result = "deny"
        return PolicyDetailedEvaluation(result, evaluations)

    @classmethod
    def load(cls, policy_input: typing.Union[pathlib.Path, str]) -> "Policy":
        """Load the specified policy from yaml."""
        try:
            body = (
                policy_input.read_text()
                if hasattr(policy_input, "read_text")
                else policy_input
            )
            raw_yaml = yaml.safe_load(body)
        except yaml.YAMLError:
            raise _errors.PolicyYamlInvalidError("Invalid policy yaml.")
        _validate_yaml(raw_yaml)
        statements = [
            Statement.from_jsonable(statement) for statement in raw_yaml["statements"]
        ]
        return Policy(statements)

    def to_jsonable(self) -> dict:
        """Serialize the policy to a JSONable object."""
        return {
            "type": "policy",
            "statements": [s.to_jsonable() for s in self.statements],
        }

    @classmethod
    def from_jsonable(cls, jsonable: dict) -> dict:
        """Deserialize the policy set from a JSONable object."""
        return cls([Statement.from_jsonable(s) for s in jsonable["statements"]])
