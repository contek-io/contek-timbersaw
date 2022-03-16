# CONTEK Timbersaw Logging Configurator

```contek-timbersaw``` is a logging configurator.

### 1. Initialization

```python
import logging
import contek_timbersaw

contek_timbersaw.setup()
logger = logging.getLogger(__name__)

logger.info('foo bar')
```
