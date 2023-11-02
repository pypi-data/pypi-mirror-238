class RefManager:
    def __init__(self):
        self.refs_dict = {}
        self.ref_id = 1

    def create_ref(self, obj):
        ref_id = self.ref_id
        self.refs_dict[ref_id] = obj
        self.ref_id += 1
        return ref_id
    
    def create_ref_with_key(self, key: str, obj):
        self.refs_dict[key] = obj
    
    def get_ref(self, refId):
        return self.refs_dict.get(refId, None)
    
def remap_credentials(credentials: dict) -> dict:
    """Remaps credentials from profiles siteconfig to the expected format from snowflake session

    Args:
        credentials (dict): Data warehouse credentials from profiles siteconfig

    Returns:
        dict: Data warehouse creadentials remapped in format that is required to create a snowpark session
    """
    new_creds = {k if k != 'dbname' else 'database': v for k, v in credentials.items() if k != 'type'}
    return new_creds