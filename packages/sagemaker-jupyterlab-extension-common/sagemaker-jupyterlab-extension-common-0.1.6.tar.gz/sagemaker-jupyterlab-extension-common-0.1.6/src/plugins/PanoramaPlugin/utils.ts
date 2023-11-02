const injectPanoramaScript = (region: string) => {
  if (!region) {
    throw new Error('Failed to get region');
  }

  const script = document.createElement('script');
  script.src = 'https://prod.pa.cdn.uis.awsstatic.com/panorama-nav-init.js';
  script.id = 'awsc-panorama-bundle';
  script.type = 'text/javascript';
  script.setAttribute(
    'data-config',
    `{"appEntity": "aws-sagemaker", "region": "${region}", "service" :"sagemaker-jupyterlab"}`,
  );
  document.head.appendChild(script);
};

export { injectPanoramaScript };
