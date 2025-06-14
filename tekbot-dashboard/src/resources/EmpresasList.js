import * as React from 'react';
import { List, Datagrid, TextField } from 'react-admin';

export const EmpresasList = props => (
  <List {...props}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="nome_fantasia" label="Nome" />
      <TextField source="cnpj" />
      <TextField source="contato" />
      <TextField source="telefone" />
    </Datagrid>
  </List>
);