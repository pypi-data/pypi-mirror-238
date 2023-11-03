import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { injectPanoramaScript } from './utils';
import { OPTIONS_TYPE, fetchApiResponse } from '../../services';
import { SAGEMAKER_CONTEXT_ENDPOINT, pluginIds } from '../../constants';

const mountPanorama = async (app: JupyterFrontEnd) => {
  try {
    await app.started;
    const jupyterLabMain = document.getElementById('main');

    const getStudioContextResponse = await fetchApiResponse(SAGEMAKER_CONTEXT_ENDPOINT, OPTIONS_TYPE.GET);
    const region = (await getStudioContextResponse.json()).region;
    if (jupyterLabMain) {
      injectPanoramaScript(region);
    } else {
      throw new Error('JupyterLab application or region not found in DOM');
    }
  } catch (err) {
    // Log panorama error
  }
};

const PanoramaPlugin: JupyterFrontEndPlugin<void> = {
  id: pluginIds.PanoramaPlugin,
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    mountPanorama(app);
  },
};

export { PanoramaPlugin };
