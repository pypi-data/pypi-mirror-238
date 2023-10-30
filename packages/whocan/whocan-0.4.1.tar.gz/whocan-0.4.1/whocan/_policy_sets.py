import dataclasses
import enum
import json
import typing

from whocan import _policies
from whocan import _environment


DEFAULT_ENV = _environment.PolicyEnvironment({})
PermissionDefiner = typing.Union[_policies.Policy, "PolicySet"]


class Operation(enum.Enum):
    """The manner in which policies should be merged."""

    UNION = "union"
    INTERSECT = "intersect"


@dataclasses.dataclass
class PolicySetDetailedEvaluation:
    """The evaluation of a policy set."""

    result: typing.Optional[str]
    favor_deny: bool
    statement_evaluations: typing.List[_policies.PolicyDetailedEvaluation]

    def __str__(self):
        """Get a string representation of the evaluation."""
        return json.dumps(dataclasses.asdict(self), indent=2)


@dataclasses.dataclass
class PolicySet:
    """A set of policies that interact to determine access."""

    policies: typing.List[PermissionDefiner]
    operation: Operation = Operation.INTERSECT
    favor_deny: bool = True

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
    ) -> PolicySetDetailedEvaluation:
        """
        Evaluate the policy to determine if it allows, denys, or makes no
        comment on the specified resource and action, providing a detailed
        evaluation of the policy set.

        :param action:
            The action being taken on the specified resource.
        :param resource:
            The resource on which the action is being taken.
        :param arguments:
            Arguments to pass into the policy before determining if
            access is allowed.
        :return:
            A detailed evaluation of the policy set.
        """
        evaluations = [
            policy.debug(action, resource, principal, arguments, env)
            for policy in self.policies
        ]
        deny_result = None
        if any(v.result == "deny" for v in evaluations):
            deny_result = "deny"
        allow_result = None
        handler = all if (self.operation == Operation.INTERSECT) else any
        if handler(v.result == "allow" for v in evaluations):
            allow_result = "allow"
        result = (
            deny_result or allow_result
            if self.favor_deny
            else allow_result or deny_result
        )
        return PolicySetDetailedEvaluation(result, self.favor_deny, evaluations)

    def to_jsonable(self) -> dict:
        """Serialize the policy set to a JSONable object."""
        return {
            "type": "policy_set",
            "operation": self.operation.value,
            "policies": [p.to_jsonable() for p in self.policies],
            "favor_deny": self.favor_deny,
        }

    @classmethod
    def from_jsonable(cls, jsonable: dict) -> dict:
        """Deserialize the policy set from a JSONable object."""
        operation = {k.value: k for k in Operation}[jsonable["operation"]]
        policies = [
            _policies.Policy.from_jsonable(p)
            if p["type"] == "policy"
            else PolicySet.from_jsonable(p)
            for p in jsonable["policies"]
        ]
        return cls(policies, operation, jsonable["favor_deny"])
