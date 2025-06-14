// src/resources/InsightsList.js
import * as React from 'react';
import {
  List,
  Datagrid,
  TextField,
  DateField,
  ReferenceField,
} from 'react-admin';

export const InsightsList = props => (
  <List {...props} title="Insights de IA">
    <Datagrid rowClick="show">
      <TextField source="id" />
      <ReferenceField
        source="chamado_id"
        reference="chamados"
        label="Chamado"
      >
        <TextField source="id" />
      </ReferenceField>
      <TextField source="resumo" />
      <TextField source="sugestoes" label="Sugestões" />
      <DateField source="data_gerado" label="Data" />
    </Datagrid>
  </List>
);
