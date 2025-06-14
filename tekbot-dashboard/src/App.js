import * as React from 'react';
import { Admin, Resource } from 'react-admin';
import dataProvider from './dataProvider';
import { ChamadosList } from './resources/ChamadosList';
import { EmpresasList } from './resources/EmpresasList';
import { MensagensList } from './resources/MensagensList';
import { InsightsList } from './resources/InsightsList';
import { TestsList } from './resources/TestsList';

export default function App() {
  return (
    <Admin dataProvider={dataProvider}>
      <Resource name="chamados" list={ChamadosList} />
      <Resource name="empresas" list={EmpresasList} />
      <Resource name="mensagens" list={MensagensList} />
      <Resource name="insights_ia" list={InsightsList} />
      <Resource name="tests" list={TestsList} />
    </Admin>
  );
}
