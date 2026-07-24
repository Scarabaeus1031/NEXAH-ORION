.PHONY: bootstrap check test integration readiness-alpha understand-stage1-alpha understand-representation-inventory-alpha understand-source-boundary-inventory-alpha understand-source-element-declaration-check-alpha slice-ii-structural-expansion-i slice-ii-structural-expansion-ii slice-ii-complete-vocabulary slice-ii-structural-summary slice-ii-structural-statistics slice-ii-certification slice-iii-relation-object slice-iii-sequential-relations slice-iii-structural-equality slice-iii-declared-cross-references slice-iii-relation-conformance slice-iii-relations-certification slice-iii-navigation-object slice-iii-navigation-construction slice-iii-navigation-conformance slice-iii-navigation-certification slice-iii-orientation-map-object slice-iii-orientation-map-construction slice-iii-orientation-map-conformance slice-iii-certification slice-iv-expression-contract slice-iv-expression-construction slice-iv-expression-conformance slice-iv-expression-certification slice-iv-certification adr release-check

bootstrap:
	./scripts/bootstrap-workspace

check:
	./scripts/check-workspace

test:
	./scripts/test

integration:
	./scripts/test-ollama-integration

readiness-alpha:
	PYTHONPATH=src python3 scripts/runtime_readiness_alpha_proof.py

understand-stage1-alpha:
	PYTHONPATH=src python3 scripts/understand_stage1_alpha_proof.py

understand-representation-inventory-alpha:
	PYTHONPATH=src python3 scripts/understand_representation_inventory_alpha_proof.py

understand-source-boundary-inventory-alpha:
	PYTHONPATH=src python3 scripts/understand_source_boundary_inventory_alpha_proof.py

understand-source-element-declaration-check-alpha:
	PYTHONPATH=src python3 scripts/understand_source_element_declaration_check_alpha_proof.py

slice-ii-structural-expansion-i:
	PYTHONPATH=src python3 scripts/slice_ii_structural_expansion_i_proofs.py

slice-ii-structural-expansion-ii:
	PYTHONPATH=src python3 scripts/slice_ii_structural_expansion_ii_proofs.py

slice-ii-complete-vocabulary:
	PYTHONPATH=src python3 scripts/slice_ii_complete_vocabulary_proof.py

slice-ii-structural-summary:
	PYTHONPATH=src python3 scripts/slice_ii_structural_summary_proof.py

slice-ii-structural-statistics:
	PYTHONPATH=src python3 scripts/slice_ii_structural_statistics_proof.py

slice-ii-certification:
	PYTHONPATH=src python3 scripts/slice_ii_certification_proof.py

slice-iii-relation-object:
	PYTHONPATH=src python3 scripts/slice_iii_relation_object_proof.py

slice-iii-sequential-relations:
	PYTHONPATH=src python3 scripts/slice_iii_sequential_relations_proof.py

slice-iii-structural-equality:
	PYTHONPATH=src python3 scripts/slice_iii_structural_equality_proof.py

slice-iii-declared-cross-references:
	PYTHONPATH=src python3 scripts/slice_iii_declared_cross_references_proof.py

slice-iii-relation-conformance:
	PYTHONPATH=src python3 scripts/slice_iii_relation_conformance_proof.py

slice-iii-relations-certification:
	PYTHONPATH=src python3 scripts/slice_iii_relations_certification_proof.py

slice-iii-navigation-object:
	PYTHONPATH=src python3 scripts/slice_iii_navigation_object_proof.py

slice-iii-navigation-construction:
	PYTHONPATH=src python3 scripts/slice_iii_navigation_construction_proof.py

slice-iii-navigation-conformance:
	PYTHONPATH=src python3 scripts/slice_iii_navigation_conformance_proof.py

slice-iii-navigation-certification:
	PYTHONPATH=src python3 scripts/slice_iii_navigation_certification_proof.py

slice-iii-orientation-map-object:
	PYTHONPATH=src python3 scripts/slice_iii_orientation_map_object_proof.py

slice-iii-orientation-map-construction:
	PYTHONPATH=src python3 scripts/slice_iii_orientation_map_construction_proof.py

slice-iii-orientation-map-conformance:
	PYTHONPATH=src python3 scripts/slice_iii_orientation_map_conformance_proof.py

slice-iii-certification:
	PYTHONPATH=src python3 scripts/slice_iii_certification_proof.py

slice-iv-expression-contract:
	PYTHONPATH=src python3 scripts/slice_iv_expression_contract_proof.py

slice-iv-expression-construction:
	PYTHONPATH=src python3 scripts/slice_iv_expression_construction_proof.py

slice-iv-expression-conformance:
	PYTHONPATH=src python3 scripts/slice_iv_expression_conformance_proof.py

slice-iv-expression-certification:
	PYTHONPATH=src python3 scripts/slice_iv_expression_certification_proof.py

slice-iv-certification:
	PYTHONPATH=src python3 scripts/slice_iv_certification_proof.py

adr:
	@test -n "$(TITLE)" || (echo "Usage: make adr TITLE='short decision title'"; exit 2)
	./scripts/new-adr "$(TITLE)"

release-check:
	./scripts/release-check --development
