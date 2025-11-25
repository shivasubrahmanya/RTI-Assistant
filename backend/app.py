def init_openai_client():
    # ... existing code ...

    import os
    import logging
    from dotenv import load_dotenv

    # Load .env explicitly from your backend path
    dotenv_path = r'c:\Users\shiva\Desktop\rti-main\backend\.env'
    # Ensure that .env values override existing environment values
    load_dotenv(dotenv_path, override=True)
    logging.info(f"Loading environment from {dotenv_path}")

    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise RuntimeError('OPENAI_API_KEY is missing. Check c:\\Users\\shiva\\Desktop\\rti-main\\backend\\.env')

    # Normalize quotes/whitespace and validate basic format
    api_key = api_key.strip().strip('"').strip("'")
    if not api_key.startswith('sk-') or len(api_key) < 40 or 'your_' in api_key.lower():
        raise RuntimeError(
            'Invalid OPENAI_API_KEY detected. Replace any placeholder with a real key from '
            'https://platform.openai.com/account/api-keys'
        )

    # Try new v1 SDK first; fall back to legacy v0 SDK if needed
    client = None
    is_v1 = False
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        is_v1 = True
        logging.info("Initialized OpenAI v1 client")
    except Exception as e:
        logging.warning(f"OpenAI v1 client unavailable ({e}); attempting legacy v0 client")
        try:
            import openai as openai_legacy
            openai_legacy.api_key = api_key
            client = openai_legacy
            is_v1 = False
            logging.info("Initialized OpenAI legacy v0 client")
        except Exception as e2:
            masked = api_key[:4] + '...' + api_key[-4:]
            raise RuntimeError(f'Failed to initialize OpenAI client with key {masked}: {e2}')

    # Sanity check to catch invalid keys or connectivity issues
    try:
        if is_v1:
            models = client.models.list()
            logging.info(f"Validated API key via v1 SDK. Models available: {len(getattr(models, 'data', []))}")
        else:
            models = client.Model.list()
            logging.info(f"Validated API key via v0 SDK. Models available: {len(models.get('data', []))}")
    except Exception as e:
        masked = api_key[:4] + '...' + api_key[-4:]
        raise RuntimeError(f'Failed to validate API key {masked}: {e}')

    return client
    # ... existing code ...