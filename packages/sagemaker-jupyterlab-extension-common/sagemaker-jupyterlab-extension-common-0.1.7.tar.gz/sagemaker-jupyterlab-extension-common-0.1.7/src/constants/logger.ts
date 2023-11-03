type SchemaDefinition = { schemaId: string; schemaVersion: number };
type SchemaDefinitions = { [schemaName: string]: SchemaDefinition };

const logSchemas: SchemaDefinitions = {
  operationalLogger: {
    schemaId: 'http://sagemaker.studio.jupyterlab.ui.log.schema',
    schemaVersion: 1,
  },
  performance: {
    schemaId: 'http://sagemaker.studio.jupyterlab.ui.performance.schema',
    schemaVersion: 1,
  },
};

const allowedSchemas = Object.keys(logSchemas).map((schemaName) => logSchemas[schemaName].schemaId);

// The server extension will be able to inject context including account id and space
// name if corresponding field is set to '__INJECT__'.
const CONTEXT_INJECT_PLACEHOLDER = '__INJECT__';

export { logSchemas, allowedSchemas, SchemaDefinition, SchemaDefinitions, CONTEXT_INJECT_PLACEHOLDER };
