# ESA SDK for Python

[![GitHub](https://img.shields.io/badge/GitHub-ESA%20Core-blue?logo=github&style=plastic)](https://github.com/experian-sales-advisor/ESA) [![GitHub](https://img.shields.io/badge/GitHub-ESA%20NextJS%20Web%20UI-blue?logo=github&style=plastic)](https://github.com/experian-sales-advisor/esa-nextjs) [![GitHub](https://img.shields.io/badge/GitHub-ESA%20Streamlit%20Web%20UI-blue?logo=github&style=plastic)](https://github.com/experian-sales-advisor/esa-streamlit)

[![GitHub](https://img.shields.io/badge/GitHub-ESA%20Python%20SDK-blue?logo=github&style=plastic)](https://github.com/experian-sales-advisor/esa-python-sdk) [![pypi](https://img.shields.io/badge/pypi-ESA%20Python%20SDK-blue?logo=pypi&style=plastic)](https://pypi.org/project/esa-python-sdk/)

[![GitHub](https://img.shields.io/badge/GitHub-ESA%20TypeScript%20SDK-blue?logo=github&style=plastic)](https://github.com/experian-sales-advisor/esa-typescript-sdk) [![npm](https://img.shields.io/badge/npm-ESA%20TypeScript%20SDK-blue?logo=npm&style=plastic)](https://www.npmjs.com/package/esa-nextjs)

[![Logo](https://experian-sales-advisor.github.io/ESA/images/ESA-Logo-whitebg.png)](https://experian-sales-advisor.github.io/ESA/)

This repository is for the [ESA](https://github.com/experian-sales-advisor/ESA) SDK for Python.

## Installation
```bash
pip install esa-python-sdk
```

## Usage

```python
from esa_python_sdk import ESAPYTHONSDK

base_uri = "http://localhost:7437"
api_key = "your_esa_api_key"

ApiClient = ESAPYTHONSDK(base_uri=base_uri, api_key=api_key)
```

Check out the ESA [Examples and Tests Notebook](https://github.com/experian-sales-advisor/ESA/blob/main/tests/tests.ipynb) for examples of how to use the ESA SDK for Python.

## More Documentation
Want to know more about ESA?  Check out our [documentation](https://experian-sales-advisor.github.io/ESA/) or [GitHub](https://github.com/experian-sales-advisor/ESA) page.
