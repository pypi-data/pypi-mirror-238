# Auto generated from translator_testing_model.yaml by pythongen.py version: 0.0.1
# Generation date: 2023-10-30T15:09:04
# Schema: Translator-Testing-Model
#
# id: https://w3id.org/TranslatorSRI/TranslatorTestingModel
# description: Data model to formalize the structure of test assets, cases, suites and related metadata
#   applied to run the diverse polymorphic testing objectives for the Biomedical Data Translator system.
# license: MIT

import dataclasses
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import Boolean, Date, Integer, String, Uriorcurie
from linkml_runtime.utils.metamodelcore import Bool, URIorCURIE, XSDDate

metamodel_version = "1.7.0"
version = "0.0.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
BIOLINK = CurieNamespace('biolink', 'https://w3id.org/biolink/')
EXAMPLE = CurieNamespace('example', 'https://example.org/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
TTM = CurieNamespace('ttm', 'https://w3id.org/TranslatorSRI/TranslatorTestingModel/')
DEFAULT_ = TTM


# Types

# Class references
class TestEntityId(URIorCURIE):
    pass


class TestMetadataId(TestEntityId):
    pass


class TestAssetId(TestEntityId):
    pass


class AcceptanceTestAssetId(TestAssetId):
    pass


class TestEdgeDataId(TestAssetId):
    pass


class TestCaseId(TestEntityId):
    pass


class TestCaseSpecificationId(TestEntityId):
    pass


class AcceptanceTestCaseId(TestCaseId):
    pass


class QuantitativeTestCaseId(TestCaseId):
    pass


class ComplianceTestCaseId(TestCaseId):
    pass


class KnowledgeGraphNavigationTestCaseId(TestCaseId):
    pass


class OneHopTestCaseId(KnowledgeGraphNavigationTestCaseId):
    pass


class TestSuiteId(TestEntityId):
    pass


class AcceptanceTestSuiteId(TestSuiteId):
    pass


class StandardsComplianceTestSuiteId(TestSuiteId):
    pass


class OneHopTestSuiteId(TestSuiteId):
    pass


class PreconditionId(TestEntityId):
    pass


@dataclass
class TestEntity(YAMLRoot):
    """
    Abstract global 'identification' class shared as a parent with all major model classes within the data model for
    Translator testing.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TTM.TestEntity
    class_class_curie: ClassVar[str] = "ttm:TestEntity"
    class_name: ClassVar[str] = "TestEntity"
    class_model_uri: ClassVar[URIRef] = TTM.TestEntity

    id: Union[str, TestEntityId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TestEntityId):
            self.id = TestEntityId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.tags, list):
            self.tags = [self.tags] if self.tags is not None else []
        self.tags = [v if isinstance(v, str) else str(v) for v in self.tags]

        super().__post_init__(**kwargs)


@dataclass
class TestMetadata(TestEntity):
    """
    Represents metadata related to (external SME, SMURF, Translator feedback, large scale batch, etc.) like the
    provenance of test assets, cases and/or suites.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TTM.TestMetadata
    class_class_curie: ClassVar[str] = "ttm:TestMetadata"
    class_name: ClassVar[str] = "TestMetadata"
    class_model_uri: ClassVar[URIRef] = TTM.TestMetadata

    id: Union[str, TestMetadataId] = None
    test_source: Optional[Union[str, "TestSourceEnum"]] = None
    test_reference: Optional[Union[str, URIorCURIE]] = None
    test_objective: Optional[Union[str, "TestObjectiveEnum"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TestMetadataId):
            self.id = TestMetadataId(self.id)

        if self.test_source is not None and not isinstance(self.test_source, TestSourceEnum):
            self.test_source = TestSourceEnum(self.test_source)

        if self.test_reference is not None and not isinstance(self.test_reference, URIorCURIE):
            self.test_reference = URIorCURIE(self.test_reference)

        if self.test_objective is not None and not isinstance(self.test_objective, TestObjectiveEnum):
            self.test_objective = TestObjectiveEnum(self.test_objective)

        super().__post_init__(**kwargs)


@dataclass
class TestAsset(TestEntity):
    """
    Represents a Test Asset, which is a single specific instance of TestCase-agnostic semantic parameters representing
    the specification of a Translator test target with inputs and (expected) outputs.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TTM.TestAsset
    class_class_curie: ClassVar[str] = "ttm:TestAsset"
    class_name: ClassVar[str] = "TestAsset"
    class_model_uri: ClassVar[URIRef] = TTM.TestAsset

    id: Union[str, TestAssetId] = None
    runner_settings: Union[str, List[str]] = None
    input_id: Optional[Union[str, URIorCURIE]] = None
    input_name: Optional[str] = None
    predicate: Optional[str] = None
    output_id: Optional[Union[str, URIorCURIE]] = None
    output_name: Optional[str] = None
    expected_output: Optional[Union[str, "ExpectedOutputEnum"]] = None
    test_issue: Optional[Union[str, "TestIssueEnum"]] = None
    semantic_severity: Optional[Union[str, "SemanticSeverityEnum"]] = None
    in_v1: Optional[Union[bool, Bool]] = None
    well_known: Optional[Union[bool, Bool]] = None
    tags: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TestAssetId):
            self.id = TestAssetId(self.id)

        if self._is_empty(self.runner_settings):
            self.MissingRequiredField("runner_settings")
        if not isinstance(self.runner_settings, list):
            self.runner_settings = [self.runner_settings] if self.runner_settings is not None else []
        self.runner_settings = [v if isinstance(v, str) else str(v) for v in self.runner_settings]

        if self.input_id is not None and not isinstance(self.input_id, URIorCURIE):
            self.input_id = URIorCURIE(self.input_id)

        if self.input_name is not None and not isinstance(self.input_name, str):
            self.input_name = str(self.input_name)

        if self.predicate is not None and not isinstance(self.predicate, str):
            self.predicate = str(self.predicate)

        if self.output_id is not None and not isinstance(self.output_id, URIorCURIE):
            self.output_id = URIorCURIE(self.output_id)

        if self.output_name is not None and not isinstance(self.output_name, str):
            self.output_name = str(self.output_name)

        if self.expected_output is not None and not isinstance(self.expected_output, ExpectedOutputEnum):
            self.expected_output = ExpectedOutputEnum(self.expected_output)

        if self.test_issue is not None and not isinstance(self.test_issue, TestIssueEnum):
            self.test_issue = TestIssueEnum(self.test_issue)

        if self.semantic_severity is not None and not isinstance(self.semantic_severity, SemanticSeverityEnum):
            self.semantic_severity = SemanticSeverityEnum(self.semantic_severity)

        if self.in_v1 is not None and not isinstance(self.in_v1, Bool):
            self.in_v1 = Bool(self.in_v1)

        if self.well_known is not None and not isinstance(self.well_known, Bool):
            self.well_known = Bool(self.well_known)

        if not isinstance(self.tags, list):
            self.tags = [self.tags] if self.tags is not None else []
        self.tags = [v if isinstance(v, str) else str(v) for v in self.tags]

        super().__post_init__(**kwargs)


@dataclass
class AcceptanceTestAsset(TestAsset):
    """
    Model derived from Jenn's test asset design and Shervin's runner JSON here as an example.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TTM.AcceptanceTestAsset
    class_class_curie: ClassVar[str] = "ttm:AcceptanceTestAsset"
    class_name: ClassVar[str] = "AcceptanceTestAsset"
    class_model_uri: ClassVar[URIRef] = TTM.AcceptanceTestAsset

    id: Union[str, AcceptanceTestAssetId] = None
    runner_settings: Union[str, List[str]] = None
    must_pass_date: Optional[Union[str, XSDDate]] = None
    must_pass_environment: Optional[Union[str, "TestEnvEnum"]] = None
    scientific_question: Optional[str] = None
    string_entry: Optional[str] = None
    direction: Optional[Union[str, "DirectionEnum"]] = None
    answer_informal_concept: Optional[str] = None
    expected_result: Optional[Union[str, "ExpectedResultsEnum"]] = None
    top_level: Optional[int] = None
    query_node: Optional[Union[str, "NodeEnum"]] = None
    notes: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AcceptanceTestAssetId):
            self.id = AcceptanceTestAssetId(self.id)

        if self.must_pass_date is not None and not isinstance(self.must_pass_date, XSDDate):
            self.must_pass_date = XSDDate(self.must_pass_date)

        if self.must_pass_environment is not None and not isinstance(self.must_pass_environment, TestEnvEnum):
            self.must_pass_environment = TestEnvEnum(self.must_pass_environment)

        if self.scientific_question is not None and not isinstance(self.scientific_question, str):
            self.scientific_question = str(self.scientific_question)

        if self.string_entry is not None and not isinstance(self.string_entry, str):
            self.string_entry = str(self.string_entry)

        if self.direction is not None and not isinstance(self.direction, DirectionEnum):
            self.direction = DirectionEnum(self.direction)

        if self.answer_informal_concept is not None and not isinstance(self.answer_informal_concept, str):
            self.answer_informal_concept = str(self.answer_informal_concept)

        if self.expected_result is not None and not isinstance(self.expected_result, ExpectedResultsEnum):
            self.expected_result = ExpectedResultsEnum(self.expected_result)

        if self.top_level is not None and not isinstance(self.top_level, int):
            self.top_level = int(self.top_level)

        if self.query_node is not None and not isinstance(self.query_node, NodeEnum):
            self.query_node = NodeEnum(self.query_node)

        if self.notes is not None and not isinstance(self.notes, str):
            self.notes = str(self.notes)

        super().__post_init__(**kwargs)


@dataclass
class TestEdgeData(TestAsset):
    """
    Represents a single Biolink Model compliant instance of a subject-predicate-object edge that can be used for
    testing.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TTM.TestEdgeData
    class_class_curie: ClassVar[str] = "ttm:TestEdgeData"
    class_name: ClassVar[str] = "TestEdgeData"
    class_model_uri: ClassVar[URIRef] = TTM.TestEdgeData

    id: Union[str, TestEdgeDataId] = None
    runner_settings: Union[str, List[str]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TestEdgeDataId):
            self.id = TestEdgeDataId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class TestCase(TestEntity):
    """
    Represents a single enumerated instance of Test Case, derived from a given collection of one or more TestAsset
    instances (the value of the 'test_assets' slot) which define the 'inputs' and 'outputs' of the TestCase, used to
    probe a particular test condition.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TTM.TestCase
    class_class_curie: ClassVar[str] = "ttm:TestCase"
    class_name: ClassVar[str] = "TestCase"
    class_model_uri: ClassVar[URIRef] = TTM.TestCase

    id: Union[str, TestCaseId] = None
    test_assets: Union[Dict[Union[str, TestAssetId], Union[dict, TestAsset]], List[Union[dict, TestAsset]]] = empty_dict()
    test_env: Optional[Union[str, "TestEnvEnum"]] = None
    test_case_type: Optional[Union[str, "TestCaseTypeEnum"]] = None
    query_type: Optional[Union[str, "QueryTypeEnum"]] = None
    preconditions: Optional[Union[Union[str, PreconditionId], List[Union[str, PreconditionId]]]] = empty_list()
    tags: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TestCaseId):
            self.id = TestCaseId(self.id)

        if self._is_empty(self.test_assets):
            self.MissingRequiredField("test_assets")
        self._normalize_inlined_as_list(slot_name="test_assets", slot_type=TestAsset, key_name="id", keyed=True)

        if self.test_env is not None and not isinstance(self.test_env, TestEnvEnum):
            self.test_env = TestEnvEnum(self.test_env)

        if self.test_case_type is not None and not isinstance(self.test_case_type, TestCaseTypeEnum):
            self.test_case_type = TestCaseTypeEnum(self.test_case_type)

        if self.query_type is not None and not isinstance(self.query_type, QueryTypeEnum):
            self.query_type = QueryTypeEnum(self.query_type)

        if not isinstance(self.preconditions, list):
            self.preconditions = [self.preconditions] if self.preconditions is not None else []
        self.preconditions = [v if isinstance(v, PreconditionId) else PreconditionId(v) for v in self.preconditions]

        if not isinstance(self.tags, list):
            self.tags = [self.tags] if self.tags is not None else []
        self.tags = [v if isinstance(v, str) else str(v) for v in self.tags]

        super().__post_init__(**kwargs)


@dataclass
class TestCaseSpecification(TestEntity):
    """
    Parameterized declaration of the Test Case generator which dynamically generates a collection of Test Cases from
    Test Assets, using applicable heuristics.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TTM.TestCaseSpecification
    class_class_curie: ClassVar[str] = "ttm:TestCaseSpecification"
    class_name: ClassVar[str] = "TestCaseSpecification"
    class_model_uri: ClassVar[URIRef] = TTM.TestCaseSpecification

    id: Union[str, TestCaseSpecificationId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TestCaseSpecificationId):
            self.id = TestCaseSpecificationId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class AcceptanceTestCase(TestCase):
    """
    See AcceptanceTestAsset above for more details.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TTM.AcceptanceTestCase
    class_class_curie: ClassVar[str] = "ttm:AcceptanceTestCase"
    class_name: ClassVar[str] = "AcceptanceTestCase"
    class_model_uri: ClassVar[URIRef] = TTM.AcceptanceTestCase

    id: Union[str, AcceptanceTestCaseId] = None
    test_assets: Union[Dict[Union[str, AcceptanceTestAssetId], Union[dict, AcceptanceTestAsset]], List[Union[dict, AcceptanceTestAsset]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AcceptanceTestCaseId):
            self.id = AcceptanceTestCaseId(self.id)

        if self._is_empty(self.test_assets):
            self.MissingRequiredField("test_assets")
        self._normalize_inlined_as_list(slot_name="test_assets", slot_type=AcceptanceTestAsset, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class QuantitativeTestCase(TestCase):
    """
    Assumed additional model from Shervin's runner JSON here as an example.  This schema is not yet complete.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TTM.QuantitativeTestCase
    class_class_curie: ClassVar[str] = "ttm:QuantitativeTestCase"
    class_name: ClassVar[str] = "QuantitativeTestCase"
    class_model_uri: ClassVar[URIRef] = TTM.QuantitativeTestCase

    id: Union[str, QuantitativeTestCaseId] = None
    test_assets: Union[Dict[Union[str, TestAssetId], Union[dict, TestAsset]], List[Union[dict, TestAsset]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, QuantitativeTestCaseId):
            self.id = QuantitativeTestCaseId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ComplianceTestCase(TestCase):
    """
    TRAPI and Biolink Model standards compliance test
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TTM.ComplianceTestCase
    class_class_curie: ClassVar[str] = "ttm:ComplianceTestCase"
    class_name: ClassVar[str] = "ComplianceTestCase"
    class_model_uri: ClassVar[URIRef] = TTM.ComplianceTestCase

    id: Union[str, ComplianceTestCaseId] = None
    test_assets: Union[Dict[Union[str, TestAssetId], Union[dict, TestAsset]], List[Union[dict, TestAsset]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ComplianceTestCaseId):
            self.id = ComplianceTestCaseId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class KnowledgeGraphNavigationTestCase(TestCase):
    """
    Knowledge Graph navigation integration test
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TTM.KnowledgeGraphNavigationTestCase
    class_class_curie: ClassVar[str] = "ttm:KnowledgeGraphNavigationTestCase"
    class_name: ClassVar[str] = "KnowledgeGraphNavigationTestCase"
    class_model_uri: ClassVar[URIRef] = TTM.KnowledgeGraphNavigationTestCase

    id: Union[str, KnowledgeGraphNavigationTestCaseId] = None
    test_assets: Union[Dict[Union[str, TestAssetId], Union[dict, TestAsset]], List[Union[dict, TestAsset]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, KnowledgeGraphNavigationTestCaseId):
            self.id = KnowledgeGraphNavigationTestCaseId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class OneHopTestCase(KnowledgeGraphNavigationTestCase):
    """
    'One Hop' Knowledge Graph navigation integration test
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TTM.OneHopTestCase
    class_class_curie: ClassVar[str] = "ttm:OneHopTestCase"
    class_name: ClassVar[str] = "OneHopTestCase"
    class_model_uri: ClassVar[URIRef] = TTM.OneHopTestCase

    id: Union[str, OneHopTestCaseId] = None
    test_assets: Union[Dict[Union[str, TestAssetId], Union[dict, TestAsset]], List[Union[dict, TestAsset]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, OneHopTestCaseId):
            self.id = OneHopTestCaseId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class TestSuite(TestEntity):
    """
    Specification of a set of Test Cases, one of either with a static list of 'test_cases' or a dynamic
    'test_case_specification' slot values. Note: at least one slot or the other, but generally not both(?) needs to be
    present.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TTM.TestSuite
    class_class_curie: ClassVar[str] = "ttm:TestSuite"
    class_name: ClassVar[str] = "TestSuite"
    class_model_uri: ClassVar[URIRef] = TTM.TestSuite

    id: Union[str, TestSuiteId] = None
    test_metadata: Optional[Union[str, TestMetadataId]] = None
    test_persona: Optional[Union[str, "TestPersonaEnum"]] = None
    test_cases: Optional[Union[Dict[Union[str, TestCaseId], Union[dict, TestCase]], List[Union[dict, TestCase]]]] = empty_dict()
    test_case_specification: Optional[Union[str, TestCaseSpecificationId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TestSuiteId):
            self.id = TestSuiteId(self.id)

        if self.test_metadata is not None and not isinstance(self.test_metadata, TestMetadataId):
            self.test_metadata = TestMetadataId(self.test_metadata)

        if self.test_persona is not None and not isinstance(self.test_persona, TestPersonaEnum):
            self.test_persona = TestPersonaEnum(self.test_persona)

        self._normalize_inlined_as_dict(slot_name="test_cases", slot_type=TestCase, key_name="id", keyed=True)

        if self.test_case_specification is not None and not isinstance(self.test_case_specification, TestCaseSpecificationId):
            self.test_case_specification = TestCaseSpecificationId(self.test_case_specification)

        super().__post_init__(**kwargs)


@dataclass
class AcceptanceTestSuite(TestSuite):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TTM.AcceptanceTestSuite
    class_class_curie: ClassVar[str] = "ttm:AcceptanceTestSuite"
    class_name: ClassVar[str] = "AcceptanceTestSuite"
    class_model_uri: ClassVar[URIRef] = TTM.AcceptanceTestSuite

    id: Union[str, AcceptanceTestSuiteId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AcceptanceTestSuiteId):
            self.id = AcceptanceTestSuiteId(self.id)

        super().__post_init__(**kwargs)


class BenchmarkTestSuite(YAMLRoot):
    """
    JsonObj(is_a='TestSuite')
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TTM.BenchmarkTestSuite
    class_class_curie: ClassVar[str] = "ttm:BenchmarkTestSuite"
    class_name: ClassVar[str] = "BenchmarkTestSuite"
    class_model_uri: ClassVar[URIRef] = TTM.BenchmarkTestSuite


@dataclass
class StandardsComplianceTestSuite(TestSuite):
    """
    Test suite for testing Translator components against releases of standards like TRAPI and the Biolink Model.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TTM.StandardsComplianceTestSuite
    class_class_curie: ClassVar[str] = "ttm:StandardsComplianceTestSuite"
    class_name: ClassVar[str] = "StandardsComplianceTestSuite"
    class_model_uri: ClassVar[URIRef] = TTM.StandardsComplianceTestSuite

    id: Union[str, StandardsComplianceTestSuiteId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, StandardsComplianceTestSuiteId):
            self.id = StandardsComplianceTestSuiteId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class OneHopTestSuite(TestSuite):
    """
    Test case for testing the integrity of "One Hop" knowledge graph retrievals sensa legacy SRI_Testing harness.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TTM.OneHopTestSuite
    class_class_curie: ClassVar[str] = "ttm:OneHopTestSuite"
    class_name: ClassVar[str] = "OneHopTestSuite"
    class_model_uri: ClassVar[URIRef] = TTM.OneHopTestSuite

    id: Union[str, OneHopTestSuiteId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, OneHopTestSuiteId):
            self.id = OneHopTestSuiteId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Precondition(TestEntity):
    """
    Represents a precondition for a TestCase
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TTM.Precondition
    class_class_curie: ClassVar[str] = "ttm:Precondition"
    class_name: ClassVar[str] = "Precondition"
    class_model_uri: ClassVar[URIRef] = TTM.Precondition

    id: Union[str, PreconditionId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PreconditionId):
            self.id = PreconditionId(self.id)

        super().__post_init__(**kwargs)


# Enumerations
class TestSourceEnum(EnumDefinitionImpl):

    SME = PermissibleValue(
        text="SME",
        description="(External) Subject Matter Expert")
    SMURF = PermissibleValue(
        text="SMURF",
        description="""Subject Matter User Reasonably Familiar, generally Translator-internal biomedical science expert""")
    GitHubUserFeedback = PermissibleValue(
        text="GitHubUserFeedback",
        description="Git hub hosted issue from which a test asset/case/suite may be derived.")
    TACT = PermissibleValue(
        text="TACT",
        description="""Technical Advisory Committee, generally posting semantic use cases as Translator Feedback issues""")
    BenchMark = PermissibleValue(
        text="BenchMark",
        description="Curated benchmark tests")
    TranslatorTeam = PermissibleValue(
        text="TranslatorTeam",
        description="Translator funded KP or ARA team generating test assets/cases/suites for their resources.")
    TestDataLocation = PermissibleValue(
        text="TestDataLocation",
        description="Current SRI_Testing-like test data edges specific to KP or ARA components")

    _defn = EnumDefinition(
        name="TestSourceEnum",
    )

class TestObjectiveEnum(EnumDefinitionImpl):

    AcceptanceTest = PermissibleValue(
        text="AcceptanceTest",
        description="Acceptance (pass/fail) test")
    BenchmarkTest = PermissibleValue(
        text="BenchmarkTest",
        description="Semantic benchmarking")
    QuantitativeTest = PermissibleValue(
        text="QuantitativeTest",
        description="Quantitative test")

    _defn = EnumDefinition(
        name="TestObjectiveEnum",
    )

class TestPersonaEnum(EnumDefinitionImpl):

    All = PermissibleValue(text="All")
    Clinical = PermissibleValue(
        text="Clinical",
        description="An MD or someone working in the clinical field.")
    LookUp = PermissibleValue(
        text="LookUp",
        description="Looking for an answer for a specific patient.")
    Mechanistic = PermissibleValue(
        text="Mechanistic",
        description="""Someone working on basic biology questions or drug discoveries where the study of the biological mechanism.""")

    _defn = EnumDefinition(
        name="TestPersonaEnum",
    )

class QueryTypeEnum(EnumDefinitionImpl):
    """
    Query
    """
    treats = PermissibleValue(text="treats")

    _defn = EnumDefinition(
        name="QueryTypeEnum",
        description="Query",
    )

class ExpectedOutputEnum(EnumDefinitionImpl):
    """
    Expected output values for instances of Test Asset or Test Cases(?). (Note: does this Enum overlap with
    'ExpectedResultsEnum' below?)
    """
    Top_Answer = PermissibleValue(text="Top_Answer")
    Acceptable = PermissibleValue(text="Acceptable")
    BadButForgivable = PermissibleValue(text="BadButForgivable")
    NeverShow = PermissibleValue(text="NeverShow")
    number_1_TopAnswer = PermissibleValue(text="number_1_TopAnswer")
    number_2_Acceptable = PermissibleValue(text="number_2_Acceptable")
    number_3_BadButForgivable = PermissibleValue(text="number_3_BadButForgivable")
    number_4_NeverShow = PermissibleValue(text="number_4_NeverShow")

    _defn = EnumDefinition(
        name="ExpectedOutputEnum",
        description="""Expected output values for instances of Test Asset or Test Cases(?). (Note: does this Enum overlap with 'ExpectedResultsEnum' below?)""",
    )

class ExpectedResultsEnum(EnumDefinitionImpl):
    """
    Does this Enum overlap with 'ExpectedOutputEnum' above?
    """
    include_good = PermissibleValue(
        text="include_good",
        description="The query should return the result in this test case")
    exclude_bad = PermissibleValue(
        text="exclude_bad",
        description="The query should not return the result in this test case")

    _defn = EnumDefinition(
        name="ExpectedResultsEnum",
        description="Does this Enum overlap with 'ExpectedOutputEnum' above?",
    )

class NodeEnum(EnumDefinitionImpl):
    """
    Target node of a Subject-Predicate-Object driven query
    """
    subject = PermissibleValue(text="subject")
    object = PermissibleValue(text="object")

    _defn = EnumDefinition(
        name="NodeEnum",
        description="Target node of a Subject-Predicate-Object driven query",
    )

class TestEnvEnum(EnumDefinitionImpl):
    """
    Testing environments within which a TestSuite is run by a TestRunner scheduled by the TestHarness.
    """
    dev = PermissibleValue(
        text="dev",
        description="Development")
    ci = PermissibleValue(
        text="ci",
        description="Continuous Integration")
    test = PermissibleValue(
        text="test",
        description="Test")
    prod = PermissibleValue(
        text="prod",
        description="Production")

    _defn = EnumDefinition(
        name="TestEnvEnum",
        description="Testing environments within which a TestSuite is run by a TestRunner scheduled by the TestHarness.",
    )

class TestCaseTypeEnum(EnumDefinitionImpl):
    """
    Enumerated tags for types of test (generally applied to a TestCase).
    """
    acceptance = PermissibleValue(
        text="acceptance",
        description="Acceptance test")
    quantitative = PermissibleValue(
        text="quantitative",
        description="Quantitative test")
    compliance = PermissibleValue(
        text="compliance",
        description="Standards compliance test")
    kg_navigation = PermissibleValue(
        text="kg_navigation",
        description="Knowledge Graph navigation integration test")
    one_hop = PermissibleValue(
        text="one_hop",
        description="One Hop navigation test")

    _defn = EnumDefinition(
        name="TestCaseTypeEnum",
        description="Enumerated tags for types of test (generally applied to a TestCase).",
    )

class TestIssueEnum(EnumDefinitionImpl):

    TMKP = PermissibleValue(
        text="TMKP",
        description="'Text Mining Knowledge Provider' generated relationship?")
    contraindications = PermissibleValue(text="contraindications")
    test_issue = PermissibleValue(text="test_issue")

    _defn = EnumDefinition(
        name="TestIssueEnum",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "causes not treats",
            PermissibleValue(text="causes not treats"))
        setattr(cls, "category too generic",
            PermissibleValue(text="category too generic"))
        setattr(cls, "chemical roles",
            PermissibleValue(text="chemical roles"))

class SemanticSeverityEnum(EnumDefinitionImpl):
    """
    From Jenn's worksheet, empty or ill defined (needs elaboration)
    """
    High = PermissibleValue(text="High")
    Low = PermissibleValue(text="Low")
    NotApplicable = PermissibleValue(text="NotApplicable")

    _defn = EnumDefinition(
        name="SemanticSeverityEnum",
        description="From Jenn's worksheet, empty or ill defined (needs elaboration)",
    )

class DirectionEnum(EnumDefinitionImpl):

    increased = PermissibleValue(text="increased")
    decreased = PermissibleValue(text="decreased")

    _defn = EnumDefinition(
        name="DirectionEnum",
    )

# Slots
class slots:
    pass

slots.runner_settings = Slot(uri=TTM.runner_settings, name="runner_settings", curie=TTM.curie('runner_settings'),
                   model_uri=TTM.runner_settings, domain=None, range=Union[str, List[str]])

slots.id = Slot(uri=SCHEMA.identifier, name="id", curie=SCHEMA.curie('identifier'),
                   model_uri=TTM.id, domain=None, range=URIRef)

slots.name = Slot(uri=SCHEMA.name, name="name", curie=SCHEMA.curie('name'),
                   model_uri=TTM.name, domain=None, range=Optional[str])

slots.description = Slot(uri=SCHEMA.description, name="description", curie=SCHEMA.curie('description'),
                   model_uri=TTM.description, domain=None, range=Optional[str])

slots.tags = Slot(uri=SCHEMA.additionalType, name="tags", curie=SCHEMA.curie('additionalType'),
                   model_uri=TTM.tags, domain=None, range=Optional[Union[str, List[str]]])

slots.test_source = Slot(uri=TTM.test_source, name="test_source", curie=TTM.curie('test_source'),
                   model_uri=TTM.test_source, domain=None, range=Optional[Union[str, "TestSourceEnum"]])

slots.test_reference = Slot(uri=TTM.test_reference, name="test_reference", curie=TTM.curie('test_reference'),
                   model_uri=TTM.test_reference, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.test_objective = Slot(uri=TTM.test_objective, name="test_objective", curie=TTM.curie('test_objective'),
                   model_uri=TTM.test_objective, domain=None, range=Optional[Union[str, "TestObjectiveEnum"]])

slots.input_id = Slot(uri=TTM.input_id, name="input_id", curie=TTM.curie('input_id'),
                   model_uri=TTM.input_id, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.input_name = Slot(uri=TTM.input_name, name="input_name", curie=TTM.curie('input_name'),
                   model_uri=TTM.input_name, domain=None, range=Optional[str])

slots.predicate = Slot(uri=TTM.predicate, name="predicate", curie=TTM.curie('predicate'),
                   model_uri=TTM.predicate, domain=None, range=Optional[str])

slots.output_id = Slot(uri=TTM.output_id, name="output_id", curie=TTM.curie('output_id'),
                   model_uri=TTM.output_id, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.output_name = Slot(uri=TTM.output_name, name="output_name", curie=TTM.curie('output_name'),
                   model_uri=TTM.output_name, domain=None, range=Optional[str])

slots.expected_output = Slot(uri=TTM.expected_output, name="expected_output", curie=TTM.curie('expected_output'),
                   model_uri=TTM.expected_output, domain=None, range=Optional[Union[str, "ExpectedOutputEnum"]])

slots.test_issue = Slot(uri=TTM.test_issue, name="test_issue", curie=TTM.curie('test_issue'),
                   model_uri=TTM.test_issue, domain=None, range=Optional[Union[str, "TestIssueEnum"]])

slots.semantic_severity = Slot(uri=TTM.semantic_severity, name="semantic_severity", curie=TTM.curie('semantic_severity'),
                   model_uri=TTM.semantic_severity, domain=None, range=Optional[Union[str, "SemanticSeverityEnum"]])

slots.in_v1 = Slot(uri=TTM.in_v1, name="in_v1", curie=TTM.curie('in_v1'),
                   model_uri=TTM.in_v1, domain=None, range=Optional[Union[bool, Bool]])

slots.well_known = Slot(uri=TTM.well_known, name="well_known", curie=TTM.curie('well_known'),
                   model_uri=TTM.well_known, domain=None, range=Optional[Union[bool, Bool]])

slots.test_metadata = Slot(uri=TTM.test_metadata, name="test_metadata", curie=TTM.curie('test_metadata'),
                   model_uri=TTM.test_metadata, domain=None, range=Optional[Union[str, TestMetadataId]])

slots.test_persona = Slot(uri=TTM.test_persona, name="test_persona", curie=TTM.curie('test_persona'),
                   model_uri=TTM.test_persona, domain=None, range=Optional[Union[str, "TestPersonaEnum"]])

slots.test_assets = Slot(uri=TTM.test_assets, name="test_assets", curie=TTM.curie('test_assets'),
                   model_uri=TTM.test_assets, domain=None, range=Union[Dict[Union[str, TestAssetId], Union[dict, TestAsset]], List[Union[dict, TestAsset]]])

slots.test_cases = Slot(uri=TTM.test_cases, name="test_cases", curie=TTM.curie('test_cases'),
                   model_uri=TTM.test_cases, domain=None, range=Optional[Union[Dict[Union[str, TestCaseId], Union[dict, TestCase]], List[Union[dict, TestCase]]]])

slots.test_case_specification = Slot(uri=TTM.test_case_specification, name="test_case_specification", curie=TTM.curie('test_case_specification'),
                   model_uri=TTM.test_case_specification, domain=None, range=Optional[Union[str, TestCaseSpecificationId]])

slots.must_pass_date = Slot(uri=TTM.must_pass_date, name="must_pass_date", curie=TTM.curie('must_pass_date'),
                   model_uri=TTM.must_pass_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.must_pass_environment = Slot(uri=TTM.must_pass_environment, name="must_pass_environment", curie=TTM.curie('must_pass_environment'),
                   model_uri=TTM.must_pass_environment, domain=None, range=Optional[Union[str, "TestEnvEnum"]])

slots.scientific_question = Slot(uri=TTM.scientific_question, name="scientific_question", curie=TTM.curie('scientific_question'),
                   model_uri=TTM.scientific_question, domain=None, range=Optional[str])

slots.string_entry = Slot(uri=TTM.string_entry, name="string_entry", curie=TTM.curie('string_entry'),
                   model_uri=TTM.string_entry, domain=None, range=Optional[str])

slots.direction = Slot(uri=TTM.direction, name="direction", curie=TTM.curie('direction'),
                   model_uri=TTM.direction, domain=None, range=Optional[Union[str, "DirectionEnum"]])

slots.answer_informal_concept = Slot(uri=TTM.answer_informal_concept, name="answer_informal_concept", curie=TTM.curie('answer_informal_concept'),
                   model_uri=TTM.answer_informal_concept, domain=None, range=Optional[str])

slots.expected_result = Slot(uri=TTM.expected_result, name="expected_result", curie=TTM.curie('expected_result'),
                   model_uri=TTM.expected_result, domain=None, range=Optional[Union[str, "ExpectedResultsEnum"]])

slots.top_level = Slot(uri=TTM.top_level, name="top_level", curie=TTM.curie('top_level'),
                   model_uri=TTM.top_level, domain=None, range=Optional[int])

slots.query_node = Slot(uri=TTM.query_node, name="query_node", curie=TTM.curie('query_node'),
                   model_uri=TTM.query_node, domain=None, range=Optional[Union[str, "NodeEnum"]])

slots.notes = Slot(uri=TTM.notes, name="notes", curie=TTM.curie('notes'),
                   model_uri=TTM.notes, domain=None, range=Optional[str])

slots.requires_trapi = Slot(uri=TTM.requires_trapi, name="requires_trapi", curie=TTM.curie('requires_trapi'),
                   model_uri=TTM.requires_trapi, domain=None, range=Optional[Union[bool, Bool]])

slots.test_env = Slot(uri=TTM.test_env, name="test_env", curie=TTM.curie('test_env'),
                   model_uri=TTM.test_env, domain=None, range=Optional[Union[str, "TestEnvEnum"]])

slots.test_case_type = Slot(uri=TTM.test_case_type, name="test_case_type", curie=TTM.curie('test_case_type'),
                   model_uri=TTM.test_case_type, domain=None, range=Optional[Union[str, "TestCaseTypeEnum"]])

slots.query_type = Slot(uri=TTM.query_type, name="query_type", curie=TTM.curie('query_type'),
                   model_uri=TTM.query_type, domain=None, range=Optional[Union[str, "QueryTypeEnum"]])

slots.preconditions = Slot(uri=TTM.preconditions, name="preconditions", curie=TTM.curie('preconditions'),
                   model_uri=TTM.preconditions, domain=None, range=Optional[Union[Union[str, PreconditionId], List[Union[str, PreconditionId]]]])

slots.TestAsset_id = Slot(uri=SCHEMA.identifier, name="TestAsset_id", curie=SCHEMA.curie('identifier'),
                   model_uri=TTM.TestAsset_id, domain=TestAsset, range=Union[str, TestAssetId])

slots.TestAsset_tags = Slot(uri=SCHEMA.additionalType, name="TestAsset_tags", curie=SCHEMA.curie('additionalType'),
                   model_uri=TTM.TestAsset_tags, domain=TestAsset, range=Optional[Union[str, List[str]]])

slots.TestAsset_runner_settings = Slot(uri=TTM.runner_settings, name="TestAsset_runner_settings", curie=TTM.curie('runner_settings'),
                   model_uri=TTM.TestAsset_runner_settings, domain=TestAsset, range=Union[str, List[str]])

slots.TestCase_test_case_type = Slot(uri=TTM.test_case_type, name="TestCase_test_case_type", curie=TTM.curie('test_case_type'),
                   model_uri=TTM.TestCase_test_case_type, domain=TestCase, range=Optional[Union[str, "TestCaseTypeEnum"]])

slots.TestCase_test_assets = Slot(uri=TTM.test_assets, name="TestCase_test_assets", curie=TTM.curie('test_assets'),
                   model_uri=TTM.TestCase_test_assets, domain=TestCase, range=Union[Dict[Union[str, TestAssetId], Union[dict, TestAsset]], List[Union[dict, TestAsset]]])

slots.TestCase_tags = Slot(uri=SCHEMA.additionalType, name="TestCase_tags", curie=SCHEMA.curie('additionalType'),
                   model_uri=TTM.TestCase_tags, domain=TestCase, range=Optional[Union[str, List[str]]])

slots.AcceptanceTestCase_test_assets = Slot(uri=TTM.test_assets, name="AcceptanceTestCase_test_assets", curie=TTM.curie('test_assets'),
                   model_uri=TTM.AcceptanceTestCase_test_assets, domain=AcceptanceTestCase, range=Union[Dict[Union[str, AcceptanceTestAssetId], Union[dict, AcceptanceTestAsset]], List[Union[dict, AcceptanceTestAsset]]])