import * as React from 'react';
import { List, Datagrid, TextField, DateField } from 'react-admin';

export const TestsList = props => (
  <List {...props}>
    <Datagrid rowClick="show">
      <TextField source="id" />
      <TextField source="name" />
      <TextField source="status" />
      <DateField source="date" />
    </Datagrid>
  </List>
);