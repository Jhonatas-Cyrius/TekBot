import * as React from 'react';
import { List, Datagrid, TextField, DateField } from 'react-admin';

export const MensagensList = props => (
  <List {...props} filter={{ chamado_id: props.filterValue || '' }}>
    <Datagrid rowClick="show">
      <TextField source="id" />
      <TextField source="chamado_id" />
      <TextField source="remetente" />
      <TextField source="conteudo" />
      <DateField source="data_hora" />
    </Datagrid>
  </List>
);