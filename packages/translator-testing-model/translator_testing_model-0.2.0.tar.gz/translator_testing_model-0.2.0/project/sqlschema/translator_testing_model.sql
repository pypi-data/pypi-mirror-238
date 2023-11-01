

CREATE TABLE "AcceptanceTestCase" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	test_env VARCHAR(4), 
	test_case_type VARCHAR(13), 
	query_type VARCHAR(6), 
	preconditions TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "ComplianceTestCase" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	test_env VARCHAR(4), 
	test_case_type VARCHAR(13), 
	query_type VARCHAR(6), 
	test_assets TEXT NOT NULL, 
	preconditions TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "KnowledgeGraphNavigationTestCase" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	test_env VARCHAR(4), 
	test_case_type VARCHAR(13), 
	query_type VARCHAR(6), 
	test_assets TEXT NOT NULL, 
	preconditions TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "OneHopTestCase" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	test_env VARCHAR(4), 
	test_case_type VARCHAR(13), 
	query_type VARCHAR(6), 
	test_assets TEXT NOT NULL, 
	preconditions TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "Precondition" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "QuantitativeTestCase" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	test_env VARCHAR(4), 
	test_case_type VARCHAR(13), 
	query_type VARCHAR(6), 
	test_assets TEXT NOT NULL, 
	preconditions TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "TestAsset" (
	name TEXT, 
	description TEXT, 
	input_id TEXT, 
	input_name TEXT, 
	predicate TEXT, 
	output_id TEXT, 
	output_name TEXT, 
	expected_output VARCHAR(25), 
	test_issue VARCHAR(20), 
	semantic_severity VARCHAR(13), 
	in_v1 BOOLEAN, 
	well_known BOOLEAN, 
	id TEXT NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE "TestCase" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	test_env VARCHAR(4), 
	test_case_type VARCHAR(13), 
	query_type VARCHAR(6), 
	test_assets TEXT NOT NULL, 
	preconditions TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "TestCaseSpecification" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "TestEdgeData" (
	name TEXT, 
	description TEXT, 
	input_id TEXT, 
	input_name TEXT, 
	predicate TEXT, 
	output_id TEXT, 
	output_name TEXT, 
	expected_output VARCHAR(25), 
	test_issue VARCHAR(20), 
	semantic_severity VARCHAR(13), 
	in_v1 BOOLEAN, 
	well_known BOOLEAN, 
	id TEXT NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE "TestMetadata" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	test_source VARCHAR(18), 
	test_reference TEXT, 
	test_objective VARCHAR(16), 
	PRIMARY KEY (id)
);

CREATE TABLE "AcceptanceTestAsset" (
	name TEXT, 
	description TEXT, 
	input_id TEXT, 
	input_name TEXT, 
	predicate TEXT, 
	output_id TEXT, 
	output_name TEXT, 
	expected_output VARCHAR(25), 
	test_issue VARCHAR(20), 
	semantic_severity VARCHAR(13), 
	in_v1 BOOLEAN, 
	well_known BOOLEAN, 
	id TEXT NOT NULL, 
	must_pass_date DATE, 
	must_pass_environment VARCHAR(4), 
	scientific_question TEXT, 
	string_entry TEXT, 
	direction VARCHAR(9), 
	answer_informal_concept TEXT, 
	expected_result VARCHAR(12), 
	top_level INTEGER, 
	query_node VARCHAR(7), 
	notes TEXT, 
	"AcceptanceTestCase_id" TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY("AcceptanceTestCase_id") REFERENCES "AcceptanceTestCase" (id)
);

CREATE TABLE "AcceptanceTestSuite" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	test_metadata TEXT, 
	test_persona VARCHAR(11), 
	test_cases TEXT, 
	test_case_specification TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(test_metadata) REFERENCES "TestMetadata" (id), 
	FOREIGN KEY(test_case_specification) REFERENCES "TestCaseSpecification" (id)
);

CREATE TABLE "OneHopTestSuite" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	test_metadata TEXT, 
	test_persona VARCHAR(11), 
	test_cases TEXT, 
	test_case_specification TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(test_metadata) REFERENCES "TestMetadata" (id), 
	FOREIGN KEY(test_case_specification) REFERENCES "TestCaseSpecification" (id)
);

CREATE TABLE "StandardsComplianceTestSuite" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	test_metadata TEXT, 
	test_persona VARCHAR(11), 
	test_cases TEXT, 
	test_case_specification TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(test_metadata) REFERENCES "TestMetadata" (id), 
	FOREIGN KEY(test_case_specification) REFERENCES "TestCaseSpecification" (id)
);

CREATE TABLE "TestSuite" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	test_metadata TEXT, 
	test_persona VARCHAR(11), 
	test_cases TEXT, 
	test_case_specification TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(test_metadata) REFERENCES "TestMetadata" (id), 
	FOREIGN KEY(test_case_specification) REFERENCES "TestCaseSpecification" (id)
);

CREATE TABLE "AcceptanceTestCase_tags" (
	backref_id TEXT, 
	tags TEXT, 
	PRIMARY KEY (backref_id, tags), 
	FOREIGN KEY(backref_id) REFERENCES "AcceptanceTestCase" (id)
);

CREATE TABLE "ComplianceTestCase_tags" (
	backref_id TEXT, 
	tags TEXT, 
	PRIMARY KEY (backref_id, tags), 
	FOREIGN KEY(backref_id) REFERENCES "ComplianceTestCase" (id)
);

CREATE TABLE "KnowledgeGraphNavigationTestCase_tags" (
	backref_id TEXT, 
	tags TEXT, 
	PRIMARY KEY (backref_id, tags), 
	FOREIGN KEY(backref_id) REFERENCES "KnowledgeGraphNavigationTestCase" (id)
);

CREATE TABLE "OneHopTestCase_tags" (
	backref_id TEXT, 
	tags TEXT, 
	PRIMARY KEY (backref_id, tags), 
	FOREIGN KEY(backref_id) REFERENCES "OneHopTestCase" (id)
);

CREATE TABLE "Precondition_tags" (
	backref_id TEXT, 
	tags TEXT, 
	PRIMARY KEY (backref_id, tags), 
	FOREIGN KEY(backref_id) REFERENCES "Precondition" (id)
);

CREATE TABLE "QuantitativeTestCase_tags" (
	backref_id TEXT, 
	tags TEXT, 
	PRIMARY KEY (backref_id, tags), 
	FOREIGN KEY(backref_id) REFERENCES "QuantitativeTestCase" (id)
);

CREATE TABLE "TestAsset_runner_settings" (
	backref_id TEXT, 
	runner_settings TEXT NOT NULL, 
	PRIMARY KEY (backref_id, runner_settings), 
	FOREIGN KEY(backref_id) REFERENCES "TestAsset" (id)
);

CREATE TABLE "TestAsset_tags" (
	backref_id TEXT, 
	tags TEXT, 
	PRIMARY KEY (backref_id, tags), 
	FOREIGN KEY(backref_id) REFERENCES "TestAsset" (id)
);

CREATE TABLE "TestCase_tags" (
	backref_id TEXT, 
	tags TEXT, 
	PRIMARY KEY (backref_id, tags), 
	FOREIGN KEY(backref_id) REFERENCES "TestCase" (id)
);

CREATE TABLE "TestCaseSpecification_tags" (
	backref_id TEXT, 
	tags TEXT, 
	PRIMARY KEY (backref_id, tags), 
	FOREIGN KEY(backref_id) REFERENCES "TestCaseSpecification" (id)
);

CREATE TABLE "TestEdgeData_runner_settings" (
	backref_id TEXT, 
	runner_settings TEXT NOT NULL, 
	PRIMARY KEY (backref_id, runner_settings), 
	FOREIGN KEY(backref_id) REFERENCES "TestEdgeData" (id)
);

CREATE TABLE "TestEdgeData_tags" (
	backref_id TEXT, 
	tags TEXT, 
	PRIMARY KEY (backref_id, tags), 
	FOREIGN KEY(backref_id) REFERENCES "TestEdgeData" (id)
);

CREATE TABLE "TestMetadata_tags" (
	backref_id TEXT, 
	tags TEXT, 
	PRIMARY KEY (backref_id, tags), 
	FOREIGN KEY(backref_id) REFERENCES "TestMetadata" (id)
);

CREATE TABLE "AcceptanceTestAsset_runner_settings" (
	backref_id TEXT, 
	runner_settings TEXT NOT NULL, 
	PRIMARY KEY (backref_id, runner_settings), 
	FOREIGN KEY(backref_id) REFERENCES "AcceptanceTestAsset" (id)
);

CREATE TABLE "AcceptanceTestAsset_tags" (
	backref_id TEXT, 
	tags TEXT, 
	PRIMARY KEY (backref_id, tags), 
	FOREIGN KEY(backref_id) REFERENCES "AcceptanceTestAsset" (id)
);

CREATE TABLE "AcceptanceTestSuite_tags" (
	backref_id TEXT, 
	tags TEXT, 
	PRIMARY KEY (backref_id, tags), 
	FOREIGN KEY(backref_id) REFERENCES "AcceptanceTestSuite" (id)
);

CREATE TABLE "OneHopTestSuite_tags" (
	backref_id TEXT, 
	tags TEXT, 
	PRIMARY KEY (backref_id, tags), 
	FOREIGN KEY(backref_id) REFERENCES "OneHopTestSuite" (id)
);

CREATE TABLE "StandardsComplianceTestSuite_tags" (
	backref_id TEXT, 
	tags TEXT, 
	PRIMARY KEY (backref_id, tags), 
	FOREIGN KEY(backref_id) REFERENCES "StandardsComplianceTestSuite" (id)
);

CREATE TABLE "TestSuite_tags" (
	backref_id TEXT, 
	tags TEXT, 
	PRIMARY KEY (backref_id, tags), 
	FOREIGN KEY(backref_id) REFERENCES "TestSuite" (id)
);
