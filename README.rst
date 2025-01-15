PyAutoBuild: PyAuto Build Server
================================

This project performs automatic building, testing and deployment of projects in the PyAuto software family:

- `PyAutoConf <https://github.com/rhayes777/PyAutoConf>`_
- `PyAutoFit <https://github.com/rhayes777/PyAutoFit>`_
- `PyAutoArray <https://github.com/Jammy2211/PyAutoArray>`_
- `PyAutoGalaxy <https://github.com/Jammy2211/PyAutoGalay>`_
- `PyAutoLens <https://github.com/Jammy2211/PyAutoLens>`_
- `PyAutoCTI <https://github.com/Jammy2211/PyAutoCTI>`_

It uses their associated workspaces:

- `autofit_workspace <https://github.com/Jammy2211/autofit_workspace>`_
- `autogalaxy_workspace <https://github.com/Jammy2211/autogalaxy_workspace>`_
- `autolens_workspace <https://github.com/Jammy2211/autolens_workspace>`_

And their test workspaces:

- `autofit_workspace_test <https://github.com/Jammy2211/autofit_workspace_test>`_
- `autogalaxy_workspace_test <https://github.com/Jammy2211/autogalaxy_workspace_test>`_
- `autolens_workspace_test <https://github.com/Jammy2211/autolens_workspace_test>`_

The build pipeline includes the following tasks:

- Package and release all projects to the test_pypi server.
- Install all test packages via pip.
- Run all project unit tests.
- Run all workspace integration test scripts.
- If successful, release packages to pypi.
- Update workspaces with new test scripts.

This automatically runs every 24 hours.