# ULedger/core.py

"""
ULedger, Inc
@file core.py
@summary SDK for ULedger's Blockchain Interaction.
@version 0.0.1
@since 0.0.1
@author Carlomagno Amaya carlomagno@uledger.io
"""

import json
import string
import requests
import logging
import hashlib
import binascii
import random
import os
from typing import List
from datetime import datetime, timezone
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

from .exceptions import (
    AtomicTimestampRetrievalFailed,
    ConnectionFailed,
    DecryptionException,
    EncryptionException,
    InvalidLanguageException,
    InvalidParameters,
    InvalidBlockchainData,
    InvalidPrivateKeyHexException,
    InvalidSearchTypeException,
    InvalidSeedException,
    InvalidWordCountException,
    InvalidWordListException,
    MessageSigningError,
    MissingAPIkey,
    MissingPrivateKeyHexException,
    ParsingError,
    PrivateKeyGenerationFailedException,
    ULRequestFailedException,
    ResponseDecodeFailed,
    SerializationError,
    SignatureVerificationError,
    Timeout,
    UnsupportedHTTPMethod,
)

class Blockchain:
    """
    Main SDK class for ULedger's Blockchain.
    Provides basic methods for interaction with the ULedger Blockchain creating, searching, updating and listing transactions and blocks.
    Also provides methods for searching blocks, transactions, and getting user history.
    """

    def __init__(self, api_key, log_level=logging.INFO, headers=None):
        """
        Initializes ULedgerBlockchain with given API key and logging level.

        :param api_key: The API key for authentication.
        :param log_level: Logging level for the SDK. Defaults to DEBUG.
        """
        if not api_key:
            raise MissingAPIkey()
        self.api_key = api_key
        self.headers = (
            headers
            if headers
            else {
                "Authorization": f"{self.api_key}",
                "Content-Type": "application/json",
            }
        )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)    
        self.bms = self._BMS(self)
        self.node = self._Node(self)

    def _send_request(self, url, method, endpoint, data=None, params=None):
        """
        Private method to send HTTP requests.

        :param url: Base URL to send the request.
        :param method: HTTP method.
        :param endpoint: Endpoint (path) to call.
        :param data: JSON Data for the request. Defaults to None.
        :param params: Parameters for the URL query string. Defaults to None.
        :return: Response from the server in JSON format.
        """
        URL = f"https://{url}/{endpoint}"

        try:
            if method == "GET":
                response = requests.get(URL, headers=self.headers, params=params)
            elif method == "POST":
                response = requests.post(
                    URL, params=params, headers=self.headers, data=json.dumps(data)
                )
            elif method == "PUT":
                response = requests.put(
                    URL, params=params, headers=self.headers, data=json.dumps(data)
                )
            else:
                raise UnsupportedHTTPMethod(method)

            response.raise_for_status()
            return response.json()

        except requests.ConnectionError:
            self.logger.error(f"Failed to connect to server.")
            raise ConnectionFailed()
        except requests.Timeout:
            self.logger.error(f"Request to server timed out.")
            raise Timeout()
        except requests.HTTPError as e:
            self.logger.error(f"HTTP Error {response.status_code}: {e}")
            raise requests.HTTPError()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to send request server. Error: {e}")
            raise ULRequestFailedException()
        except ValueError:
            self.logger.error(f"Failed to decode response. ")
            raise ResponseDecodeFailed()

    def _bms_version(self):
        return self.bms._version()

    def bms_info(self):
        """
        Retrieve blockchain management services information.\
        :return: List of blocks.
        """
        return self.bms._service_info()

    def public_blocks(self, limit=10, offset=0, sort=True, trim=True):
        """
        Retrieve list public blocks based on the given parameters.

        :param limit: Limit for the number of results, defaults to 10.
        :param offset: Offset for paginating results. Useful for fetching subsequent pages of results, defaults to 0.
        :param sort: Sorting criteria for the results. It determines the order in which blocks are returned, defaults to True.
        :param trim:  If set, it trims the response to essentials, removing extra data, defaults to True.
        :return: List of blocks.
        """
        return self.bms._get_blocks(limit, offset, sort, trim)

    def list_blocks(self, blockchain_id, limit=10, offset=0, sort=True, trim=True):
        """
        Retrieve blocks from a blockchain.

        :param blockchain_id: Unique ID of the blockchain .
        :param limit: Limit for the number of results, defaults to 10.
        :param offset: Offset for paginating results, defaults to 0.
        :param sort: Sort results, defaults to True.
        :param trim: Trim the response to essentials, defaults to True.
        :return: List of blocks in the blockchain.
        """
        return self.bms._get_blockchain_blocks(blockchain_id, limit, offset, sort, trim)

    def _create_blockchain(
        self, name, height=0, minting_index=0, timestamp=None, public=False
    ):
        return self.bms._create_blockchain(
            name, height, minting_index, timestamp, public=public
        )

    def _search_blockchain(
        self, identifier, search_type="id", limit=10, offset=0, sort=True, public=False
    ):
        return self.bms._search_blockchain(
            identifier, search_type, limit, offset, sort, public
        )

    def _update_blockchain(self, blockchain_id, blockchain_height, public):
        return self.bms._update_blockchain(blockchain_id, blockchain_height, public)

    def _list_blockchains(self, limit=10, offset=0, sort=True, public=True):
        return self.bms._list_blockchains(limit, offset, sort, public)

    def search_block(self, block_id):
        """
        Search a block by its unique ID.

        :param block_id: Unique identifier of the block.
        :return: Response from the server containing block details.
        """
        return self.bms._search_block(block_id)

    def search_transaction(self, transaction_id, trim=True):
        """
        Search a transaction by its unique ID.

        :param transaction_id: Unique identifier of the transaction.
        :param trim: Trim the response to essentials. Defaults to False.
        :return: Response from the server containing transaction details.
        """
        return self.bms._search_transaction(transaction_id, trim)

    def list_transactions(
        self, blockchain_id=None, limit=10, offset=0, sort=True, trim=True
    ):
        """
        Retrieve transactions from a blockchain based on the given parameters.
        If no blockchain_id is given, function will returin the list of available public transactions.

        :param blockchain_id: Optional identifier of the blockchain to filter transactions.
        :param limit: Limit for the number of results. Defaults to 10.
        :param offset: Offset for paginating results. Defaults to 0.
        :param sort: Sort results. Defaults to True.
        :param trim: Trim the response to essentials. Defaults to True.
        :return: List of transactions.
        """
        return self.bms._get_transactions(blockchain_id, limit, offset, sort, trim)

    def block_transactions(self, block_id, limit=10, offset=0, sort=True, trim=True):
        """
        Retrieve transactions of a specific block.

        :param block_id: Identifier of the block.
        :param limit: Limit for the number of results. Defaults to 10.
        :param offset: Offset for paginating results. Defaults to 0.
        :param sort: Sort results. Defaults to True.
        :param trim: Trim the response to essentials. Defaults to True.
        :return: List of transactions in the block.
        """
        return self.bms._get_block_transactions(block_id, limit, offset, sort, trim)

    def user_history(
        self, blockchain_id, user_id, limit=10, offset=0, sort=True, trim=True
    ):
        """
        Retrieve transaction history of a specific user.

        :param blockchain_id: Identifier of the blockchain where the user's transactions are stored.
        :param user_id: Identifier of the user whose transaction history is being queried.
        :param limit: Limit for the number of results. Defaults to 10.
        :param offset: Offset for paginating results. Defaults to 0.
        :param sort: Sort results. Defaults to True.
        :param trim: Trim the response to essentials. Defaults to True.
        :return: List of transactions associated with the user.
        """
        return self.bms._get_user_history(
            blockchain_id, user_id, limit, offset, sort, trim
        )

    def create_transaction(
        self,
        node_address: str,
        blockchain_id: str,
        node_id: str,
        to: str,
        payload,
        wallet,
        payload_type="DATA",
    ):
        """
        Create a new transaction within the blockchain network.

        :param node_address: The address of the node responsible for processing the transaction.
        :param blockchain_id: Identifier of the blockchain where the transaction will be added.
        :param payload: The content or data to be included in the transaction.
        :param payload_type: The type of payload being included in the transaction (default is "DATA").

        :return: The id for the created transaction.
        """
        return self._Node._create_transaction(
            self,
            node_address,
            blockchain_id,
            node_id,
            to,
            payload,
            wallet,
            payload_type
        )

    def _validate_words(self, seed_phrase):
        words = seed_phrase.split()

        for word in words:
            if word != word.lower():
                return False
        return True
    
    def _get_seed_words(self, num_words, language):
        """
        Generates a cryptographically secure word list for the seed phrase.

        Args:
            num_words (int): The number of words desired, supported arguments are 12, 15, 18, 21, 24.
            language (str): The language to generate word lists, supported languages: english, chinese, french, italian, japanese, korean, spanish.

        Returns:
            str: A string containing the generated words separated by spaces.
        """
        return self.wallet._generate_words(num_words, language)

    def _create(self, seed_phrase, language="english"):
        return self.wallet._create(seed_phrase, language)

    class _BMS:
        """
        Nested class for Blockchain Management System (BMS) specific operations.
        Provides methods for operations related to blockchains, blocks, and transactions.
        """

        def __init__(self, sdk_instance, base_url="dev-services.uledger.net/api/v1/bms"):
            """
            Initializes BMS with an SDK instance and a base URL.

            :param sdk_instance: Instance of the main SDK class.
            :param base_url: Base URL for BMS API. Defaults to "dev-services.uledger.net/api/v1/bms".
            """

            self.sdk = sdk_instance
            self.BASE_URL = base_url

        def _version(self):
            endpoint = "version"
            response = self.sdk._send_request(self.BASE_URL, "GET", endpoint)
            return response

        # To do, endpoint doesnt return a proper json response
        def _create_blockchain(
            self, name, height, minting_index, timestamp=None, public=True
        ):
            """
            Creates a blockchain with the given parameters.

            :param name: Name of the blockchain.
            :param id: Unique identifier for the blockchain.
            :param height: Blockchain height. Defaults to 0.
            :param minting_index: Index of minting. Defaults to 0.
            :param timestamp: Timestamp for the blockchain creation in UTC format. Defaults to current time.
            :param public: Flag to indicate if the blockchain is public. Defaults to True.
            :return: Response from the server.
            """
            endpoint = "blockchain"

            if timestamp is None:
                current_utc_time = datetime.now(timezone.utc)
                timestamp = current_utc_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

            data = {
                "blockchain_name": name,
                "blockchain_height": height,
                "minting_index": minting_index,
                "public": public,
            }
            try:
                response = self.sdk._send_request(
                    self.BASE_URL, "POST", endpoint, data=data
                )
                response.raise_for_status()
            except requests.RequestException as e:
                raise ULRequestFailedException(f"Failed to create blockchain. Error: {e}")
            except ValueError as e:
                raise InvalidBlockchainData(f"Invalid data provided for blockchain creation. Error: {e}")
            
            return response 

        def _service_info(self):
            """
            Get service information.

            :return: Response from the server containing service details.
            """
            endpoint = "service"
            response = self.sdk._send_request(self.BASE_URL, "GET", endpoint)
            return response

        def _get_blocks(self, limit, offset, sort, trim):
            """
            Retrieve blocks based on the given parameters.

            :param limit: Limit for the number of results.
            :param offset: Offset for paginating results. Useful for fetching subsequent pages of results.
            :param sort: Sorting criteria for the results. It determines the order in which blocks are returned.
            :param trim:  If set, it trims the response to essentials, removing extra data..
            :return: List of blocks.
            """

            endpoint = "block"
            params = {"limit": limit, "offset": offset, "sort": sort, "trim": trim}
            try:
                response = self.sdk._send_request(
                    self.BASE_URL, "GET", endpoint, params=params
                )
            except requests.RequestException as e:
                raise ULRequestFailedException(f"Failed to to retrieve blocks. Error {e}")
            except ValueError as e:
                raise InvalidParameters(f"Invalid paramenters for block retrieval. Error :{e}")
            return response

        def _get_blockchain_blocks(self, blockchain_id, limit, offset, sort, trim):
            """
            Retrieve blocks from a blockchain.

            :param blockchain_id: Unique ID of the blockchain .
            :param limit: Limit for the number of results.
            :param offset: Offset for paginating results.
            :param sort: Sort results.
            :param trim: Trim the response to essentials.
            :return: List of blocks in the blockchain.
            """
            endpoint = f"block/{blockchain_id}/preview"
            params = {"limit": limit, "offset": offset, "sort": sort, "trim": trim}
            try:
                response = self.sdk._send_request(
                    self.BASE_URL, "GET", endpoint, params=params
                )
            except requests.RequestException as e:
                raise ULRequestFailedException(f"Failed to retrieve blocks from blockchain. Error: {e}")
            except ValueError as e:
                raise InvalidParameters(f"Invalid parameters provided for blockchain block retrieval.")
            return response

        def _search_blockchain(
            self, identifier, search_type, limit, offset, sort, public
        ):
            """
            Search a blockchain based on given parameters.

            :param identifier: Unique identifier for searching the blockchain.
            :param search_type: Type of search. Either 'id' or 'name'. Defaults to 'id'.
            :param limit: Limit for the number of results. Defaults to 10.
            :param offset: Offset for paginating results. Defaults to 0.
            :param sort: Sort results. Defaults to True.
            :param public: Search in public blockchains. Defaults to False.
            :return: Response from the server.
            """
            if search_type not in ["id", "name"]:
                raise InvalidSearchTypeException()

            endpoint = f"blockchain/{identifier}/{search_type}"
            params = {"limit": limit, "offset": offset, "sort": sort, "public": public}
            try:
                response = self.sdk._send_request(
                    self.BASE_URL, "GET", endpoint, params=params
                )
                response.raise_for_status()
            except requests.RequestException as e:
                raise ULRequestFailedException(f"Faiuled to retrieve blocks from blockchain. Error: {e}")
            except ValueError as e:
                raise InvalidParameters(f"Invalid parameters provided for blockchain block retrieval. Error: {e}")
            return response

        def _update_blockchain(self, blockchain_id, blockchain_height, public):
            """
            Update a blockchain with new height and public flag.

            :param blockchain_id: Unique identifier of the blockchain.
            :param blockchain_height: New height for the blockchain.
            :param public: Flag to indicate if the blockchain is public.
            :return: Response from the server.
            """
            endpoint = f"blockchain/{blockchain_id}"
            data = {"blockchain_height": blockchain_height, "public": public}
            try:
                response = self.sdk._send_request(self.BASE_URL, "PUT", endpoint, data=data)
                response.raise_for_status()
            except requests.RequestException as e:
                raise ULRequestFailedException(f"Failed to update blockhain. Error: {e}")
            except ValueError as e:
                raise InvalidParameters(f"Invalid parameters for update blockchain.")
            return response

        def _list_blockchains(self, limit=10, offset=0, sort=True, public=True):
            """
            List all blockchains based on given parameters.

            :param limit: Limit for the number of results. Defaults to 10.
            :param offset: Offset for paginating results. Defaults to 0.
            :param sort: Sort results. Defaults to True.
            :param public: List public blockchains. Defaults to True.
            :return: List of blockchains.
            """
            endpoint = "blockchain"
            params = {"limit": limit, "offset": offset, "sort": sort, "public": public}
            try:
                response = self.sdk._send_request(
                    self.BASE_URL, "GET", endpoint, params=params
                )
                response.raise_for_status()
            except requests.RequestException as e:
                raise ULRequestFailedException(f"Failed to list blockhains. Error: {e}")
            except ValueError as e:
                raise InvalidParameters(f"Invalid parameters for list blockchains.")
            return response

        def _search_block(self, block_id):
            """
            Search a block by its unique ID.

            :param block_id: Unique identifier of the block.
            :return: Response from the server containing block details.
            """
            endpoint = f"block/{block_id}/list"
            try:
                response = self.sdk._send_request(self.BASE_URL, "GET", endpoint)
            except requests.RequestException as e:
                raise ULRequestFailedException(f"Failed to search block. Error: {e}")
            except ValueError as e:
                raise InvalidParameters(f"Invalid parameters for search block.")
            return response

        def _search_transaction(self, transaction_id, trim):
            """
            Search a transaction by its unique ID.

            :param transaction_id: Unique identifier of the transaction.
            :param trim: Trim the response to essentials. Defaults to False.
            :return: Response from the server containing transaction details.
            """
            endpoint = f"transaction/{transaction_id}/list?trim={str(trim).lower()}"
            try:
                response = self.sdk._send_request(self.BASE_URL, "GET", endpoint)
            except requests.RequestException as e:
                raise ULRequestFailedException(f"Failed to search transaction. Error: {e}")
            except ValueError as e:
                raise InvalidParameters(f"Invalid parameters for search transaction.")
            return response

        def _get_transactions(
            self, blockchain_id=None, limit=10, offset=0, sort=True, trim=True
        ):
            """
            Retrieve transactions based on the given parameters.

            :param blockchain_id: Optional identifier of the blockchain to filter transactions.
            :param limit: Limit for the number of results. Defaults to 10.
            :param offset: Offset for paginating results. Defaults to 0.
            :param sort: Sort results. Defaults to True.
            :param trim: Trim the response to essentials. Defaults to True.
            :return: List of transactions.
            """
            try:
                if blockchain_id:
                    endpoint = f"transaction/{blockchain_id}/preview?limit={limit}&offset={offset}&sort={str(sort).lower()}&trim={str(trim).lower()}"
                else:  # If no network name is provided, fetch public transactions
                    endpoint = f"transaction?limit={limit}&offset={offset}&sort={str(sort).lower()}&trim={str(trim).lower()}"
                response = self.sdk._send_request(self.BASE_URL, "GET", endpoint)
            except requests.RequestException as e:
                raise ULRequestFailedException(f"Failed to get transactions. Error: {e}")
            except ValueError as e:
                raise InvalidParameters(f"Invalid parameters for get transactions.")
            return response

        def _get_block_transactions(
            self, block_id, limit=10, offset=0, sort=True, trim=True
        ):
            """
            Retrieve transactions of a specific block.

            :param block_id: Identifier of the block.
            :param limit: Limit for the number of results. Defaults to 10.
            :param offset: Offset for paginating results. Defaults to 0.
            :param sort: Sort results. Defaults to True.
            :param trim: Trim the response to essentials. Defaults to True.
            :return: List of transactions in the block.
            """
            try:
                endpoint = f"transaction/{block_id}/block?limit={limit}&offset={offset}&sort={str(sort).lower()}&trim={str(trim).lower()}"
                response = self.sdk._send_request(self.BASE_URL, "GET", endpoint)
            except requests.RequestException as e:
                raise ULRequestFailedException(f"Failed to get block transactions. Error: {e}")
            except ValueError as e:
                raise InvalidParameters(f"Invalid parameters for get block transactions.")
            return response

        def _get_user_history(
            self, blockchain_id, user_id, limit=1, offset=0, sort=True, trim=True
        ):
            """
            Retrieve transaction history of a specific user.

            :param blockchain_id: Identifier of the blockchain where the user's transactions are stored.
            :param user_id: Identifier of the user whose transaction history is being queried.
            :param limit: Limit for the number of results. Defaults to 10.
            :param offset: Offset for paginating results. Defaults to 0.
            :param sort: Sort results. Defaults to True.
            :param trim: Trim the response to essentials. Defaults to True.
            :return: List of transactions associated with the user.
            """
            try:
                endpoint = f"/user/{blockchain_id}/{user_id}"
                params = {"limit": limit, "offset": offset, "sort": sort, "trim": trim}
                response = self.sdk._send_request(
                    self.BASE_URL, "GET", endpoint, params=params
                )
                response.raise_for_status()
            except requests.RequestException as e:
                raise ULRequestFailedException(f"Failed to get transactions. Error: {e}")
            except ValueError as e:
                raise InvalidParameters(f"Invalid parameters for get transactions.")
            return response

    class _Node:
        """
        Nested class for Node specific operations.
        Provides methods for operations related to transactions, node management, etc.
        """

        def __init__(self, sdk_instance):
            self.sdk = sdk_instance
            self.headers = {
                "Content-Type": "application/json",
            }
            """
            Initializes BMS with an SDK instance and a base URL.

            :param sdk_instance: Instance of the main SDK class.
            :param base_url: Base URL for BMS API. Defaults to "dev-services.uledger.net/api/v1/bms".
            """

            self.sdk = sdk_instance

        def _create_transaction(
            self,
            node_address,
            blockchain_id,
            node_id,
            to,
            payload,
            wallet,
            payload_type
        ):
            
            #Retrieveing timestamp from ACS.
            url = f'https://dev-services.uledger.net/api/v1/acs/timestamp?nodeId={node_id}'
            response = requests.get(url)
            if response.status_code == 200:
                response_data = json.loads(response.text)
                timestamp = str(response_data.get('timestamp')) + '_' + str(response_data.get('timestamp_index'))
            else:
                raise AtomicTimestampRetrievalFailed(response.status_code, "Failed to retrieve timestamp.")

            url = f"https://{node_address}/blockchain/{blockchain_id}/transaction"
            # Creating and populating data.
            data = {
                "to": to,
                "from": wallet.get_address(),
                "atomicTimestamp": timestamp,
                "payload": payload,
                "senderSignature": wallet.sign_message(json.dumps(payload, separators=(",",":"))+timestamp),
                "payloadType": payload_type,
            }
            try:
                response = requests.post(
                    url, data=json.dumps(data)
                )
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                raise Exception(f"Failed to create transaction. Error: {e}")
            except ValueError as e:
                raise InvalidParameters(f"Invalid parameters to create transaction.")
            
            return response.json()

class Wallet:
    """
    This class is the representation for the wallets in the ULedger Blockchain.
    They are used to sign transactions and verify signatures, as well as to register a wallet in the blockchain.
    """

    _private_key_hex: str
    _public_key_hex: str
    _address: str
    _seed_phrase: List[str]
    _private_key: ec.EllipticCurvePrivateKey
    _public_key: ec.EllipticCurvePublicKey

    def __init__(
        self, private_key_hex: str, seedPhrase: List[str] = []
    ):
        """
        Initializes a ULedgerWallet instance with the given private key and seed phrase,
        and derives the public key and address based on the private key.
        :param private_key_hex: The private key in hexadecimal
        :param seedPhrase: The seed phrase used to generate the private key (optional)
        """
        if not all (c in string.hexdigits for c in private_key_hex):
            raise InvalidPrivateKeyHexException()
        self._private_key_hex = private_key_hex
        self._seed_phrase = seedPhrase
        # Generate private key object then derive public key and address
        try:
            self._private_key = ec.derive_private_key(
                int(private_key_hex, 16),
                ec.SECP256K1(),
            )
        except Exception as e:
            raise PrivateKeyGenerationFailedException(f"Failed to generate the private key. Error {e}")
        self._public_key =  self._private_key.public_key()
        self._public_key_hex = self._public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint
        ).hex()
        self._address = hashlib.sha256(self._public_key_hex.encode('utf-8')).hexdigest()

    def get_public_key_hex(self) -> str:
        """
        Method to get the public key in hexadecimal format.
        :return: The public key in hexadecimal format.
        """
        return self._public_key_hex
    
    def get_address(self) -> str:
        """
        Method to get the wallet address, which is the SHA256 hash of the public key.
        :return: The wallet address.
        """
        return self._address
    
    @classmethod
    def from_dict(cls, data: dict[str, str]) -> 'Wallet':
        """
        Method to create a ULedgerWallet instance from a dictionary.
        :param data: The dictionary containing the data to create the wallet, which must contain the private key hex as 'privateKeyHex' and the optional seed phrase as 'seedPhrase'.
        :return: A new ULedgerWallet instance.
        """
        # Check if the required data is present in the dictionary.
        if 'privateKeyHex' not in data:
            raise MissingPrivateKeyHexException("Missing private key hex.")
        
        private_key_hex = data.get('privateKeyHex')
        seed_phrase = data.get('seedPhrase', [])
        
        # Create a new ULedgerWallet instance with the extracted data.
        wallet = cls(private_key_hex=private_key_hex, seedPhrase=seed_phrase)
        
        return wallet
    
    def to_dict(self) -> dict[str, str]:
        """
        Method to convert the wallet to a dictionary.
        :return: A dictionary containing the wallet data with the private key hex as 'privateKeyHex', the public key hex as 'publicKeyHex', the wallet address as 'address', and the seed phrase as 'seedPhrase'.
        """
        return {
            'privateKeyHex': self._private_key_hex,
            'seedPhrase': self._seed_phrase,
            'publicKeyHex': self._public_key_hex,
            'address': self._address,
        }
    
    def sign_message(self, message: str) -> str:
        """
        Method to sign a message with the wallet's private key, it relies on the secp256k1 elliptic curve and the SHA256 hash function.
        :param message: The message to sign.
        :return: The signature in hexadecimal format (DER Format)
        """
        try: 
            signature = self._private_key.sign(
                message.encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
            )
            return binascii.hexlify(signature).decode('utf-8')
        except Exception as e:
            raise MessageSigningError(f"Error signing message: {e}")
        
    def verify_signature(self, message:str, signature:str) -> bool:
        """
        Method to verify a signature with the wallet's public key, it relies on the secp256k1 elliptic curve and the SHA256 hash function
        :param message: The message to verify.
        :param signature: The signature in hexadecimal format (DER Format)
        :return: True if the signature is valid, False otherwise.
        """
        try:
            self._public_key.verify(
                binascii.unhexlify(signature),
                message.encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except Exception as e:
            raise SignatureVerificationError(f"Error verifying the signature: {e}")
        
    #TODO Remove the node_url dependency here and substitute it with a proxy entry.
    def register(self, blockchain_id: str, node_url: str) -> None:
        """
        Method to register the wallet in the blockchain, this is a required step to use the wallet for signing transactions in the blockchain network.
        :param blockchain_id: The unique identifier of the blockchain.
        :param node_url: The URL of the node to register the wallet.
        :return: None
        """
        #TODO Modify this and use a single function to send requests.
        try:
            url = f'https://{node_url}/blockchain/{blockchain_id}/wallet'
            data = {
                "publicKey": f"{self._public_key_hex}"
            }
            response = requests.post(url, data=json.dumps(data))
            response.raise_for_status()
            
        except requests.exceptions.RequestException as e:
                raise Exception(f"Unable to register wallet. Error: {e}")
        except ValueError as e:
            raise InvalidParameters(f"Invalid paramenters to register wallet. Error: {e}")

class WalletGenerator:
    """
    Class for generating ULedger Wallet instances and seed phrases.
    """

    VALID_WORD_COUNTS = [12, 15, 18, 21, 24]
    MIN_SEED_WORDS = 12
    MAX_SEED_WORDS = 24
    VALID_LANGUAGES = ['es', 'en', 'pt', 'fr', 'it']
    seed_words_list: dict[str, list[str]] = {}


    @staticmethod
    def get_seed_words(count: int, language: str = 'en') -> list[str]:
        """
        Generates a cryptographically secure word list for the seed phrase.
        :param count: The number of words desired, supported arguments are 12, 15, 18, 21, 24.
        :param language: The language to generate word lists, supported languages: en, pt, fr, es and it
        :return: A list containing the generated words.
        """
        if language not in WalletGenerator.VALID_LANGUAGES:
            raise InvalidLanguageException()

        if language not in WalletGenerator.seed_words_list:
            # Load word lists if not already loaded
            WalletGenerator._load_word_lists(language)

        if count < WalletGenerator.MIN_SEED_WORDS or count > WalletGenerator.MAX_SEED_WORDS:
            raise InvalidWordCountException()

        seed_words_data = WalletGenerator.seed_words_list.get(language.strip().lower())

        if not seed_words_data:
            raise InvalidWordListException()

        words = seed_words_data.copy()
        random_words = []

        for _ in range(count):
            random_index = random.randint(0, len(words) - 1)
            random_words.append(words[random_index])

            # Remove the selected word from the list to avoid duplicates
            words.pop(random_index)

        return random_words

    @staticmethod
    def _load_word_lists(language: str = 'en') -> None:
        """
        Loads the word lists from the seed words files.
        :param language: The language to load the word list, supported languages: en, pt, fr, es and it
        """
        dir_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(dir_path, 'words', f'{language}.txt')
        with open(file_path, 'r') as f:
            WalletGenerator.seed_words_list[language] = [line.strip() for line in f]
    
    @staticmethod
    def create(seed_phrase: List[str], language: str) -> 'Wallet':
        """
        Generates a Wallet instance from a seed phrase, need to provide the language used to generate the seed phrase for validation purposes
        :param seed_phrase: The seed phrase used to generate the private key.
        :param language: The language used to generate the seed phrase.
        :return: A new Wallet instance.
        """
        if language not in WalletGenerator.VALID_LANGUAGES:
            raise InvalidLanguageException(f"Invalid language. {language} not supported.")
        
        if not WalletGenerator._validate_seed_phrase(seed_phrase):
            raise InvalidWordCountException("The provided seed phrase has an invalid number of words.")
        
        if not WalletGenerator._validate_words(seed_phrase, language):
            raise InvalidSeedException(
                "The provided seed phrase is not valid, check encoding, language and lower case."
            )
        seed = ' '.join(seed_phrase)
        # Master key is the hex representation of the SHA256 hash of the seed phrase
        master_key = hashlib.sha256(seed.encode('utf-8')).hexdigest()
        return Wallet(master_key, seed_phrase)
    
    @staticmethod
    def _validate_seed_phrase(seed_phrase: List[str]) -> bool:
        """
        Validates the seed phrase length.
        :param seed_phrase: The seed phrase to validate.
        """
        num_words = len(seed_phrase)
        if num_words not in WalletGenerator.VALID_WORD_COUNTS:
            return False
        return True
    
    @staticmethod
    def _validate_words(seed_phrase: List[str], language: str = 'en') -> bool:
        """
        Validates the seed phrase words against the word list per language.
        :param seed_phrase: The seed phrase to validate.
        :param language: The language used to generate the seed phrase.
        :return: True if the seed phrase is valid, False otherwise.
        """
        if language not  in WalletGenerator.seed_words_list:  # Load word lists if not already loaded
            WalletGenerator._load_word_lists(language)

        valid_words = WalletGenerator.seed_words_list.get(language.lower())
        if not valid_words:
            return False

        for word in seed_phrase:
            if word != word.lower():
                return False
            if word not in valid_words:
                return False

        return True
    
# TODO Remove WalletFactory class and pass to Wallet Class.
class WalletFactory:
    """
    Class for serializing and deserializing ULedgerWallet instances.
    """

    @staticmethod
    def serialize(wallet: Wallet, password: str =None) -> str:
        """
        Serializes a Wallet instance to a string representation based in JSON format,
        if a password is provided, the wallet data will be encrypted using AES-GCM.
        :param wallet: The wallet to serialize.
        :param password: The password to encrypt the wallet data.
        :return: A string representation of the wallet.
        """
        try:
            serialized_data = json.dumps(wallet.to_dict())
        except Exception as e:
            raise SerializationError(f"Error serializing the wallet data: {e}")


        if password and len(password) > 0:
            try:
                salt = os.urandom(16)
                iv = os.urandom(16)
                key = hashlib.scrypt(
                    password.encode(),
                    salt=salt,
                    n=16384,
                    r=8,
                    p=1,
                    dklen=32
                )
                cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
                encryptor = cipher.encryptor()
                encrypted_data = encryptor.update(serialized_data.encode()) + encryptor.finalize()
                serialized_data = f"{salt.hex()}.{iv.hex()}.{encryptor.tag.hex()}.{encrypted_data.hex()}"
            except Exception as e:
                raise EncryptionException(f"Encryption failed: {e}")


        return serialized_data
    
    @staticmethod
    def deserialize(wallet_representation: str, password: str = None) -> 'Wallet':
        """
        Deserializes a Wallet instance from a string representation based in JSON format,
        if a password is provided, the wallet data will be decrypted using AES-GCM (must match the password used to encrypt the wallet).
        :param wallet_representation: The string representation of the wallet.
        :param password: The password to decrypt the wallet data.
        :return: A new Wallet instance.
        """

        serialized_data = wallet_representation
        if password:
            try:
                salt_hex, iv_hex, tag_hex, encrypted_data_hex = serialized_data.split('.')
                salt = bytes.fromhex(salt_hex)
                iv = bytes.fromhex(iv_hex)
                tag = bytes.fromhex(tag_hex)
                encrypted_data = bytes.fromhex(encrypted_data_hex)
                key = hashlib.scrypt(
                    password.encode(),
                    salt=salt,
                    n=16384,
                    r=8,
                    p=1,
                    dklen=32
                )
                cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
                decryptor = cipher.decryptor()
                decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
                serialized_data = decrypted_data.decode()
            except Exception as e:
                raise DecryptionException(f"Decryption failed. Possible invalid password: {e}")

        try:
            wallet_dict = json.loads(serialized_data)
            return Wallet.from_dict(wallet_dict)
        except Exception as e:
            raise ParsingError(f"Error parsing the wallet data. Malformed structure: {e}")
