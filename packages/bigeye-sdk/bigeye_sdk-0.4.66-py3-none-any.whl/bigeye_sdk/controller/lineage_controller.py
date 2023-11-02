from typing import List, Dict, Tuple, Union

from bigeye_sdk.model.delta_facade import SimpleDeltaConfiguration
from bigeye_sdk.model.enums import MatchType
from bigeye_sdk.functions.search_and_match_functions import wildcard_search, fuzzy_match
from bigeye_sdk.functions.table_functions import fully_qualified_table_to_elements
from bigeye_sdk.generated.com.bigeye.models.generated import (
    DataNode,
    Table,
    Integration,
    LineageRelationship,
    TableauWorkbook,
    Source,
    Schema,
    ComparisonTableConfiguration,
)
from bigeye_sdk.log import get_logger
from bigeye_sdk.client.datawatch_client import DatawatchClient
from bigeye_sdk.model.protobuf_enum_facade import SimpleDataNodeType

log = get_logger(__file__)


class LineageController:
    def __init__(self, client: DatawatchClient):
        self.client = client
        self.sources_by_name_ix: Dict[str, Source] = self.client.get_sources_by_name()

    def get_table_by_name(self, entity_name: str) -> Table:
        warehouse, schema, entity_name = fully_qualified_table_to_elements(entity_name)
        table: Table = self.client.get_tables(
            schema=[schema], table_name=[entity_name]
        ).tables[0]
        return table

    def get_tableau_workbook_by_name(
        self, entity_name: str, integration_name: str
    ) -> TableauWorkbook:
        integration: Integration = [
            i for i in self.client.get_integrations() if i.name == integration_name
        ][0]
        workbook = [
            w
            for w in self.client.get_integration_entities(integration_id=integration.id)
            if w.name == entity_name
        ][0]
        return workbook

    def create_node_by_name(self, entity_name: str, integration_name: str) -> DataNode:
        """Create a lineage node for an entity"""
        if not integration_name:
            table = self.get_table_by_name(entity_name=entity_name)
            log.info(f"Creating lineage node for table: {entity_name}")
            entity_id = table.id
            node_type = SimpleDataNodeType.TABLE.to_datawatch_object()

        else:
            workbook = self.get_tableau_workbook_by_name(
                entity_name=entity_name, integration_name=integration_name
            )
            log.info(f"Creating lineage node for entity: {workbook.name}")
            entity_id = workbook.id
            node_type = SimpleDataNodeType.TABLEAU.to_datawatch_object()

        return self.client.create_data_node(
            node_type=node_type, node_entity_id=entity_id
        )

    def delete_node_by_name(self, entity_name: str, integration_name: str):
        """Delete a lineage node for an entity"""
        if not integration_name:
            table = self.get_table_by_name(entity_name=entity_name)
            node_id = table.data_node_id
            log.info(f"Deleting lineage node for table: {table.name}")
        else:
            workbook = self.get_tableau_workbook_by_name(
                entity_name=entity_name, integration_name=integration_name
            )
            node_id = workbook.data_node_id
            log.info(f"Deleting lineage node for table: {workbook.name}")

        self.client.delete_data_node(data_node_id=node_id)

    def create_relation_from_name(
        self, upstream_table_name: str, downstream_table_name: str
    ) -> LineageRelationship:
        """Create a lineage relationship for 2 entities"""
        warehouse, u_schema, u_table_name = fully_qualified_table_to_elements(
            upstream_table_name
        )
        warehouse, d_schema, d_table_name = fully_qualified_table_to_elements(
            downstream_table_name
        )

        upstream: Table = self.client.get_tables(
            schema=[u_schema], table_name=[u_table_name]
        ).tables[0]
        downstream: Table = self.client.get_tables(
            schema=[d_schema], table_name=[d_table_name]
        ).tables[0]

        log.info(
            f"Creating relationship from {upstream_table_name} to {downstream_table_name}"
        )

        return self.client.create_table_lineage_relationship(
            upstream_data_node_id=upstream.data_node_id,
            downstream_data_node_id=downstream.data_node_id,
        )

    def delete_relationships_by_name(self, entity_name: str, integration_name: str):
        """Deletes all relationships for a node by name."""
        if integration_name:
            workbook = self.get_tableau_workbook_by_name(
                entity_name=entity_name, integration_name=integration_name
            )
            node_id = workbook.data_node_id
            log.info(
                f"Deleting all lineage relationships for workbook: {workbook.name}"
            )
        else:
            table = self.get_table_by_name(entity_name=entity_name)
            node_id = table.data_node_id
            log.info(f"Deleting all lineage relationships for table: {table.name}")

        self.client.delete_lineage_relationship_for_node(data_node_id=node_id)

    def get_tables_from_selector(self, selector: str) -> List[Table]:
        # Split selectors into patterns
        source_pattern, schema_pattern, table_pattern = fully_qualified_table_to_elements(selector)

        # Only take source ids that match pattern
        source_ids = [
            source.id
            for source_name, source in self.sources_by_name_ix.items()
            if source_name
            in wildcard_search(search_string=source_pattern, content=[source_name])
        ]

        # Only take schemas from those sources that match pattern
        schemas_by_name_ix: Dict[str, Schema] = {
            s.name: s for s in self.client.get_schemas(warehouse_id=source_ids).schemas
        }
        schema_ids = [
            schema.id
            for schema_name, schema in schemas_by_name_ix.items()
            if schema_name
            in wildcard_search(search_string=schema_pattern, content=[schema_name])
        ]

        # Only take tables from those schemas that match pattern
        tables_by_name_ix: Dict[str, Table] = {
            t.name: t for t in self.client.get_tables(schema_id=schema_ids).tables
        }
        tables = [
            table
            for table_name, table in tables_by_name_ix.items()
            if table_name
            in wildcard_search(search_string=table_pattern, content=[table_name])
        ]

        return tables

    @staticmethod
    def infer_relationships_from_lists_of_tables(
        upstream: List[Table],
        downstream: List[Table],
        match_type: MatchType = MatchType.STRICT,
    ) -> List[Tuple[Table, Table]]:
        # Index tables by name
        u_tables_by_name_ix = {u.name.lower(): u for u in upstream}
        d_tables_by_name_ix = {d.name.lower(): d for d in downstream}

        matching_tables: List[Tuple[Table, Table]] = []
        if match_type == MatchType.STRICT:
            for u_table in upstream:
                matching_downstream_table = next(
                    (
                        d_table
                        for d_table in downstream
                        if d_table.name.lower() == u_table.name.lower()
                    ),
                    None,
                )
                if matching_downstream_table:
                    matching_tables.append((u_table, matching_downstream_table))
        elif match_type == MatchType.FUZZY:
            for u_table in upstream:
                matching_downstream_tables = fuzzy_match(
                    search_string=u_table.name.lower(),
                    contents=[d_table.name.lower() for d_table in downstream],
                    min_match_score=95,
                )
                if matching_downstream_tables:
                    for match in matching_downstream_tables:
                        matching_tables.append(
                            (
                                u_tables_by_name_ix[match[0]],
                                d_tables_by_name_ix[match[1]],
                            )
                        )
        return matching_tables

    def create_relation_from_tables(self, upstream: Table, downstream: Table):
        node_type = SimpleDataNodeType.TABLE.to_datawatch_object()
        if upstream.data_node_id and downstream.data_node_id:
            self.client.create_table_lineage_relationship(upstream_data_node_id=upstream.data_node_id,
                                                          downstream_data_node_id=downstream.data_node_id)
        elif upstream.data_node_id and not downstream.data_node_id:
            d_node = self.client.create_data_node(node_type=node_type, node_entity_id=downstream.id)
            self.client.create_table_lineage_relationship(upstream_data_node_id=upstream.data_node_id,
                                                          downstream_data_node_id=d_node.id)
        elif not upstream.data_node_id and downstream.data_node_id:
            u_node = self.client.create_data_node(node_type=node_type, node_entity_id=upstream.id)
            self.client.create_table_lineage_relationship(upstream_data_node_id=u_node.id,
                                                          downstream_data_node_id=downstream.data_node_id)
        else:
            u_node = self.client.create_data_node(node_type=node_type, node_entity_id=upstream.id)
            d_node = self.client.create_data_node(node_type=node_type, node_entity_id=downstream.id)
            self.client.create_table_lineage_relationship(upstream_data_node_id=u_node.id,
                                                          downstream_data_node_id=d_node.id)

    def create_relations_from_delta_configuration(
            self, delta_configurations: Union[List[SimpleDeltaConfiguration], List[ComparisonTableConfiguration]]
    ):
        for dc in delta_configurations:
            source_table = self.client.get_tables(ids=[dc.source_table_id]).tables[0]
            target_table = self.client.get_tables(ids=[dc.target_table_id]).tables[0]
            try:
                self.create_relation_from_tables(upstream=source_table, downstream=target_table)
            except Exception as e:
                log.warning(f'Failed to create lineage relationship between upstream table: {source_table.name} '
                            f'and downstream table: {target_table.name}. Exception: {e}')
