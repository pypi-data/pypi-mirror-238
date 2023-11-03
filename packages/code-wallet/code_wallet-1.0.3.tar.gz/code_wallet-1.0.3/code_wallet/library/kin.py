import base58
from code_wallet.library.publickey import PublicKey

class Kin:
    """ Represents the Kin cryptocurrency with operations to handle whole and fractional units. """
    
    decimals = 5
    quarks_per_kin = 10**decimals
    mint_address = "kinXdEcpDQeHPEuQnqmUgtYykqKGVFq6CeVX5iAHJq6"
    mint = PublicKey.from_base58(mint_address)
    zero = None  # We'll initialize these after defining the class
    one = None
    max_value = None
    min_value = None
    
    def __init__(self, whole, quarks=0):
        self.whole = whole
        self.quarks = quarks
        self._normalize()
    
    def _normalize(self):
        """ Normalizes the Kin values ensuring the `quarks` value is within the valid range.
            Any overflow is added to the `whole` value.
        """
        extra_whole, self.quarks = divmod(self.quarks, Kin.quarks_per_kin)
        self.whole += extra_whole
    
    def to_quarks(self):
        return self.whole * Kin.quarks_per_kin + self.quarks
    
    def to_decimal(self):
        return self.whole + self.quarks / Kin.quarks_per_kin
    
    @classmethod
    def from_quarks(cls, quarks):
        whole, remaining_quarks = divmod(quarks, cls.quarks_per_kin)
        return cls(whole, remaining_quarks)
    
    @classmethod
    def from_decimal(cls, decimal_value):
        quarks = round(decimal_value * cls.quarks_per_kin)
        return cls.from_quarks(quarks)
    
    def add(self, other):
        result_quarks = self.to_quarks() + other.to_quarks()
        return Kin.from_quarks(result_quarks)
    
    def subtract(self, other):
        result_quarks = self.to_quarks() - other.to_quarks()
        return Kin.from_quarks(result_quarks)
    
    def multiply(self, factor):
        result_quarks = self.to_quarks() * factor
        return Kin.from_quarks(result_quarks)
    
    def divide(self, divisor):
        # Note: Using integer division which truncates towards zero.
        result_quarks = self.to_quarks() // divisor
        return Kin.from_quarks(result_quarks)


# Initializing class-level constants
Kin.zero = Kin(0, 0)
Kin.one = Kin(1, 0)
Kin.max_value = Kin(2**63 - 1, Kin.quarks_per_kin - 1)  # Max for a 64-bit integer
Kin.min_value = Kin(-2**63, 0)  # Min for a 64-bit integer