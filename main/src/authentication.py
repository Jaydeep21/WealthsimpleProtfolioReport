import wealthsimple, settings
from logger import Logger

class Authentication:
    def __init__(self):
        self.ws = self._authenticate_wealthsimple()
        self.logger = Logger("Authentication")

    def _authenticate_wealthsimple(self):
        """Authenticate with Wealthsimple using credentials from config"""
        def my_two_factor_function():
            MFACode = ""
            while not MFACode:
                # Obtain user input and ensure it is not empty
                MFACode = input("Enter 2FA code: ")
            return MFACode
        
        try:
            username = settings.USERNAME
            password = settings.PASSWORD
            
            if username == 'your_email@example.com' or password == 'your_password':
                self.logger.error("Please update your config.ini file with valid credentials")
                exit(1)
                
            return wealthsimple.WSTrade(
                username,
                password,
                two_factor_callback=my_two_factor_function,
            )
        except Exception as e:
            self.logger.error(f"Authentication failed: {str(e)}")
            exit(1)
    def get_account_type(self, id):
        """Determine account type from ID"""
        if "crypto" in id.lower():
            return "CRYPTO"
        elif "fhsa" in id.lower():
            return "FSHA"    
        elif "tfsa" in id.lower():
            return "TFSA"
        elif "non-registered" in id.lower():
            return "NON-REGISTERED"
        elif "rrsp" in id.lower():
            return "RRSP"
        else:
            return "UNKNOWN"
    def get_holdings(self):
        """Get all account holdings from Wealthsimple"""
        try:
            accounts = self.ws.get_accounts()
            self.logger.info(f"Found {len(accounts)} accounts")
            positions_by_account = {}
            for account in accounts:
                id = account["id"]
                account_type = self.get_account_type(id)
                self.logger.info(f"Processing account: {account_type}")
                
                try:
                    positions = self.ws.get_positions(id=id)
                    positions_by_account[account_type] = positions
                    self.logger.info(f"Found {len(positions)} positions in {account_type}")
                    
                    for position in positions:
                        symbol = position.get('stock', {}).get('symbol')
                        if symbol:
                            self.logger.info(f"Found position: {symbol} in {account_type}")
                except Exception as e:
                    self.logger.error(f"Error getting positions for account {account_type}: {str(e)}")
            
            return positions_by_account
            
        except Exception as e:
            self.logger.error(f"Error getting accounts: {str(e)}")
            return {}