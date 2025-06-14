import * as React from 'react';
import { List, Datagrid, TextField, DateField } from 'react-admin';

export const ChamadosList = props => (
  <List {...props}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="empresa_id" />
      <TextField source="tipo_problema" />
      <TextField source="prioridade" />
      <TextField source="status" />
      <DateField source="data_criacao" />
      <DateField source="data_fechamento" />
    </Datagrid>
  </List>
);