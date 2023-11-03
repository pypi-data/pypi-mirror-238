class InvalidSeedException(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidWordCountException(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidLanguageException(ValueError):
    def __init__(self, message="Invalid language. Supported languages: en, pt, fr, es, and it."):
        super().__init(message)

class InvalidWordListException(ValueError):
    def __init__(self, message="Invalid word list for the specified language."):
        super().__init(message)

class MissingAPIkey(Exception):
    def __init__(self, message= "API key must be provided."):
        super()._＿init__(message)

class ConnectionFailed(Exception):
    def __init__(self, message="Failed to connect to the server."):
        super().__init(message)

class Timeout(Exception):
    def __init__(self, message="Request to the server timed out."):
        super().__init(message)

class ULRequestFailedException(Exception):
    def __init__(self, message="Failed to send the request to the server."):
        super().__init(message)

class ResponseDecodeFailed(Exception):
    def __init__(self, message="Failed to decode the response."):
        super().__init(message)

class BlockchainCreationFailed(Exception):
    def __init__(self, message="Failed to create the blockchain."):
        super().__init(message)

class InvalidBlockchainData(Exception):
    def __init__(self, message="Invalid data provided for blockchain creation."):
        super().__init(message)

class UnsupportedHTTPMethod(Exception):
    def __init__(self, method):
        super().__init(f"Unsupported HTTP method: {method}")

class BlocksRetrievalFailed(Exception):
    def __init__(self, message="Failed to retrieve blocks."):
        super().__init(message)

class InvalidParameters(Exception):
    def __init__(self, message="Invalid parameters provided for block retrieval."):
        super().__init(message)

class BlockchainBlocksRetrievalFailedException(Exception):
    def __init__(self, message="Failed to retrieve blocks from the blockchain."):
        super().__init(message)

class InvalidSearchTypeException(Exception):
    def __init__(self, message="Invalid search_type. It must be either 'id' or 'name'."):
        super().__init(message)

class AtomicTimestampRetrievalFailed(Exception):
    def __init__(self, status_code, message="Failed to retrieve the atomic timestamp."):
        self.status_code = status_code
        super().__init(message)

class InvalidPrivateKeyHexException(Exception):
    def __init__(self, message="Invalid private key hex. It must be a valid hexadecimal string."):
        super().__init(message)

class PrivateKeyGenerationFailedException(Exception):
    def __init__(self, message="Failed to generate the private key."):
        super().__init(message)

class MissingPrivateKeyHexException(ValueError):
    def __init__(self, message="Missing private key hex in the dictionary."):
        super().__init(message)

class MessageSigningError(Exception):
    def __init__(self, message="Error signing the message."):
        super().__init(message)

class SignatureVerificationError(Exception):
    def __init__(self, message="Error verifying the signature."):
        super().__init(message)

class SerializationError(Exception):
    def __init__(self, message="Error serializing the wallet data."):
        super().__init(message)

class DecryptionException(ValueError):
    def __init__(self, message="Decryption failed. Possible invalid password."):
        super().__init(message)

class EncryptionException(ValueError):
    def __init__(self, message="Encryption failed."):
        super().__init(message)

class ParsingError(ValueError):
    def __init__(self, message="Error parsing the wallet data. Malformed structure."):
        super().__init(message)
