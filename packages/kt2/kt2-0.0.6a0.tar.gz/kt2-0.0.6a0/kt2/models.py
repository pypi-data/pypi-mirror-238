import typing

from fhir.resources.R4B import fhirtypes
from fhir.resources.R4B.activitydefinition import ActivityDefinition
from fhir.resources.R4B.careteam import CareTeam, CareTeamParticipant
from fhir.resources.R4B.endpoint import Endpoint
from fhir.resources.R4B.extension import Extension  # noqa
from fhir.resources.R4B.identifier import Identifier  # noqa
from fhir.resources.R4B.meta import Meta
from fhir.resources.R4B.organization import Organization
from fhir.resources.R4B.patient import Patient
from fhir.resources.R4B.practitioner import Practitioner
from fhir.resources.R4B.reference import Reference  # noqa
from fhir.resources.R4B.task import Task
from pydantic import Field

if typing.TYPE_CHECKING:
    from pydantic.types import CallableGenerator


class PersonMixin:
    @property
    def primary_email(self) -> str:
        return next(
            (contact.value for contact in self.telecom if contact.system == 'email'), ''
        )

    @property
    def first_name(self) -> str:
        return " ".join(
            next((humanname.given for humanname in self.name if humanname.given), '')
        )

    @property
    def middle_name(self) -> str:
        return " ".join(
            next((humanname.prefix for humanname in self.name if humanname.prefix), '')
        )

    @property
    def last_name(self) -> str:
        return next(
            (humanname.family for humanname in self.name if humanname.family), ''
        )

    @property
    def display_name(self) -> str:
        names = [self.first_name, self.middle_name, self.last_name]
        return ' '.join([name for name in names if name])


class KT2ActivityDefinition(ActivityDefinition):
    """
    Koppeltaal structure of ActivityDefinition
    """

    meta: fhirtypes.MetaType = Field(
        Meta(
            profile=[
                "http://koppeltaal.nl/fhir/StructureDefinition/KT2ActivityDefinition"
            ]
        ),
        alias="meta",
        title="Metadata about the resource",
        description=(
            "The metadata about the resource. This is content that is maintained by"
            " the infrastructure. Changes to the content might not always be "
            "associated with version changes to the resource."
        ),
        # if property is element of this resource.
        element_property=True,
    )


class KT2Task(Task):
    """
    Koppeltaal structure of Task

    Changes:

    - Task.partOf `KT2Task`: Reference(KT2Task) ..
    - Task.for `KT2Patient`: Reference(KT2Patient) 1..
    - Task.requester `KT2Practitioner`: Reference(KT2Practitioner) ..
    - Task.owner `KT2CareTeam | KT2Patient | KT2Practitioner`: Reference(KT2CareTeam | KT2Patient | KT2Practitioner) 1..
    """

    meta: fhirtypes.MetaType = Field(
        Meta(
            profile=["http://koppeltaal.nl/fhir/StructureDefinition/KT2TaskDefinition"]
        ),
        alias="meta",
        title="Metadata about the resource",
        description=(
            "The metadata about the resource. This is content that is maintained by"
            " the infrastructure. Changes to the content might not always be "
            "associated with version changes to the resource."
        ),
        # if property is element of this resource.
        element_property=True,
    )

    partOf: typing.List[fhirtypes.ReferenceType] = Field(
        None,
        alias="partOf",
        title="Composite task",
        description="Task that this particular task is part of.",
        # if property is element of this resource.
        element_property=True,
        # note: Listed Resource Type(s) should be allowed as Reference.
        enum_reference_types=["KT2Task"],
    )

    for_fhir: fhirtypes.ReferenceType = Field(
        None,
        alias="for",
        title="Beneficiary of the Task",
        description=(
            "The entity who benefits from the performance of the service specified "
            "in the task (e.g., the patient)."
        ),
        # if property is element of this resource.
        element_property=True,
        # note: Listed Resource Type(s) should be allowed as Reference.
        enum_reference_types=["KT2Patient"],
    )

    requester: fhirtypes.ReferenceType = Field(
        None,
        alias="requester",
        title="Who is asking for task to be done",
        description="The creator of the task.",
        # if property is element of this resource.
        element_property=True,
        # note: Listed Resource Type(s) should be allowed as Reference.
        enum_reference_types=["KT2Practitioner"],
    )

    owner: fhirtypes.ReferenceType = Field(
        None,
        alias="owner",
        title="Responsible individual",
        description="Party responsible for managing task execution.",
        # if property is element of this resource.
        element_property=True,
        # note: Listed Resource Type(s) should be allowed as Reference.
        enum_reference_types=["KT2CareTeam", "KT2Patient", "KT2Practitioner"],
    )


class KT2Endpoint(Endpoint):
    """
    Koppeltaal structure of Endpoint

    Changes:
    - Endpoint.managingOrganization `KT2Organization`: Reference(KT2Organization) ..
    """

    meta: fhirtypes.MetaType = Field(
        Meta(
            profile=[
                "http://koppeltaal.nl/fhir/StructureDefinition/KT2EndpointDefinition"
            ]
        ),
        alias="meta",
        title="Metadata about the resource",
        description=(
            "The metadata about the resource. This is content that is maintained by"
            " the infrastructure. Changes to the content might not always be "
            "associated with version changes to the resource."
        ),
        # if property is element of this resource.
        element_property=True,
    )

    managingOrganization: fhirtypes.ReferenceType = Field(
        None,
        alias="managingOrganization",
        title=(
            "Organization that manages this endpoint (might not be the organization"
            " that exposes the endpoint)"
        ),
        description=(
            "The organization that manages this endpoint (even if technically "
            "another organization is hosting this in the cloud, it is the "
            "organization associated with the data)."
        ),
        # if property is element of this resource.
        element_property=True,
        # note: Listed Resource Type(s) should be allowed as Reference.
        enum_reference_types=["KT2Organization"],
    )


class KT2CareTeamParticipant(CareTeamParticipant):
    """Koppeltaal structure for CareTeamParticipant

    Changes:
    - CareTeamParticipant.member `KT2Practitioner`: Reference(KT2Practitioner) ..
    """

    meta: fhirtypes.MetaType = Field(
        Meta(
            profile=[
                "http://koppeltaal.nl/fhir/StructureDefinition/KT2CareTeamParticipantDefinition"
            ]
        ),
        alias="meta",
        title="Metadata about the resource",
        description=(
            "The metadata about the resource. This is content that is maintained by"
            " the infrastructure. Changes to the content might not always be "
            "associated with version changes to the resource."
        ),
        # if property is element of this resource.
        element_property=True,
    )

    member: fhirtypes.ReferenceType = Field(
        None,
        alias="member",
        title="Who is involved",
        description=(
            "The specific person or organization who is participating/expected to "
            "participate in the care team."
        ),
        # if property is element of this resource.
        element_property=True,
        # note: Listed Resource Type(s) should be allowed as Reference.
        enum_reference_types=["KT2Practitioner"],
    )


class KT2CareTeamParticipantType(fhirtypes.AbstractType):
    """
    Custom abstract type for CareTeamParticipantType

    Args:
        fhirtypes `AbstractType`: KT2CareTeamParticipant AbstractType mapping
    """

    __resource_type__ = "KT2CareTeamParticipant"

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        from fhir.resources import fhirtypesvalidators

        yield getattr(fhirtypesvalidators, "CareTeamParticipant".lower() + "_validator")


class KT2CareTeam(CareTeam):
    """
    Koppeltaal structure of CareTeam

    Changes:
    - CareTeam.subject `KT2Patient`: Reference(KT2Patient) ..
    - CareTeam.participant.member `KT2Practitioner`: Reference(KT2Practitioner) ..
    - CareTeam.managingOrganization `KT2Organization`: Reference(KT2Organization) ..1
    """

    meta: fhirtypes.MetaType = Field(
        Meta(
            profile=[
                "http://koppeltaal.nl/fhir/StructureDefinition/KT2CareTeamDefinition"
            ]
        ),
        alias="meta",
        title="Metadata about the resource",
        description=(
            "The metadata about the resource. This is content that is maintained by"
            " the infrastructure. Changes to the content might not always be "
            "associated with version changes to the resource."
        ),
        # if property is element of this resource.
        element_property=True,
    )

    subject: fhirtypes.ReferenceType = Field(
        None,
        alias="subject",
        title="Who care team is for",
        description=(
            "Identifies the patient or group whose intended care is handled by the "
            "team."
        ),
        # if property is element of this resource.
        element_property=True,
        # note: Listed Resource Type(s) should be allowed as Reference.
        enum_reference_types=["KT2Patient"],
    )

    participant: typing.List[KT2CareTeamParticipantType] = Field(
        None,
        alias="participant",
        title="Members of the team",
        description=(
            "Identifies all people and organizations who are expected to be "
            "involved in the care team."
        ),
        # if property is element of this resource.
        element_property=True,
    )

    managingOrganization: typing.List[fhirtypes.ReferenceType] = Field(
        None,
        alias="managingOrganization",
        title="Organization responsible for the care team",
        description="The organization responsible for the care team.",
        # if property is element of this resource.
        element_property=True,
        # note: Listed Resource Type(s) should be allowed as Reference.
        enum_reference_types=["KT2Organization"],
    )


class KT2Patient(PersonMixin, Patient):
    """
    Koppeltaal structure of Patient

    Changes:
    - Patient.managingOrganization `KT2Organization`: Reference(KT2Organization) ..
    """

    meta: fhirtypes.MetaType = Field(
        Meta(
            profile=[
                "http://koppeltaal.nl/fhir/StructureDefinition/KT2PatientDefinition"
            ]
        ),
        alias="meta",
        title="Metadata about the resource",
        description=(
            "The metadata about the resource. This is content that is maintained by"
            " the infrastructure. Changes to the content might not always be "
            "associated with version changes to the resource."
        ),
        # if property is element of this resource.
        element_property=True,
    )

    managingOrganization: fhirtypes.ReferenceType = Field(
        None,
        alias="managingOrganization",
        title="Organization that is the custodian of the patient record",
        description=None,
        # if property is element of this resource.
        element_property=True,
        # note: Listed Resource Type(s) should be allowed as Reference.
        enum_reference_types=["KT2Organization"],
    )


class KT2Practitioner(PersonMixin, Practitioner):
    """
    Koppeltaal structure of Practitioner

    Changes:
    - No profile changes
    """

    meta: fhirtypes.MetaType = Field(
        Meta(
            profile=[
                "http://koppeltaal.nl/fhir/StructureDefinition/KT2PractitionerDefinition"
            ]
        ),
        alias="meta",
        title="Metadata about the resource",
        description=(
            "The metadata about the resource. This is content that is maintained by"
            " the infrastructure. Changes to the content might not always be "
            "associated with version changes to the resource."
        ),
        # if property is element of this resource.
        element_property=True,
    )


class KT2Organization(Organization):
    """
    Koppeltaal structure of Organization

    Changes:
    - Organization.partOf `KT2Organization`: Reference(KT2Organization) ..
    - Organization.endpoint `KT2Endpoint`: Reference(KT2Endpoint) ..0
    """

    meta: fhirtypes.MetaType = Field(
        Meta(
            profile=[
                "http://koppeltaal.nl/fhir/StructureDefinition/KT2OrganizationDefinition"
            ]
        ),
        alias="meta",
        title="Metadata about the resource",
        description=(
            "The metadata about the resource. This is content that is maintained by"
            " the infrastructure. Changes to the content might not always be "
            "associated with version changes to the resource."
        ),
        # if property is element of this resource.
        element_property=True,
    )

    partOf: fhirtypes.ReferenceType = Field(
        None,
        alias="partOf",
        title="The organization of which this organization forms a part",
        description=None,
        # if property is element of this resource.
        element_property=True,
        # note: Listed Resource Type(s) should be allowed as Reference.
        enum_reference_types=["KT2Organization"],
    )

    endpoint: typing.List[fhirtypes.ReferenceType] = Field(
        None,
        alias="endpoint",
        title=(
            "Technical endpoints providing access to services operated for the "
            "organization"
        ),
        description=None,
        # if property is element of this resource.
        element_property=True,
        # note: Listed Resource Type(s) should be allowed as Reference.
        enum_reference_types=["KT2Endpoint"],
    )
