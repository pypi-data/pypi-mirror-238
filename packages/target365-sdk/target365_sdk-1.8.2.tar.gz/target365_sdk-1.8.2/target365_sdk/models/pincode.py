from .model import Model

class Pincode(Model):

    def _accepted_params(self):
        return [
            'transactionId',
            'recipient',
            'sender',
            'prefixText',
            'suffixText',
            'pincodeLength',
        ]
