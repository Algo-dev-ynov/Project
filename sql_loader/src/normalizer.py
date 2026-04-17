import json


class SQLValueNormalizer:
    """
    Utility class used to normalize Python values before SQL insertion.

    This class ensures that values coming from MongoDB are converted into
    SQL-compatible formats:
    - None stays None
    - lists and dictionaries are converted to JSON strings
    - unsupported objects are converted to strings
    """

    @staticmethod
    def normalize(value):
        """
        Convert a Python value into a SQL-compatible value.

        Args:


            value: The value extracted from a MongoDB document.

        Returns:

        
            A normalized value that can be inserted into MariaDB.
        """
        if value is None:
            return None
        if isinstance(value, (list, dict)):
            return json.dumps(value, ensure_ascii=False)
        return str(value) if not isinstance(value, (int, float, str)) else value