# serializer 
def serialize(doc) -> dict:
    data = {}
    for key, value in doc.model_dump().items():
        if isinstance(value, dict) and '$ref' in str(value):
            # Skip unresolved link references
            continue
        data[key] = value
    
    # Handle the user link separately — just store the ID string
    if hasattr(doc, 'user') and doc.user is not None:
        try:
            if hasattr(doc.user, 'id'):
                data['user_id'] = str(doc.user.id)
            else:
                data['user_id'] = str(doc.user.ref.id)
        except Exception:
            pass
        data.pop('user', None)  # remove the raw link object
    
    data['id'] = str(doc.id)
    return data