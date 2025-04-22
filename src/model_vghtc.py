"""
This module is statically coupled with VghtcOsccSchema
Thus there is no need to dynamically pass in the self.schema object
"""
from typing import Dict, Any, List
from .schema import VghtcOsccSchema


S = VghtcOsccSchema


class CalculateVghtcOscc:

    def main(self, attributes: Dict[str, str]) -> Dict[str, Any]:

        attributes = CalculateStage().main(attributes)

        return attributes


class Calculate:

    REQUIRED_KEYS: List[str]
    attributes: Dict[str, Any]

    def main(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        self.attributes = attributes.copy()

        if not self.has_required_keys():
            return self.attributes

        self.calculate()

        return self.attributes

    def has_required_keys(self) -> bool:
        for key in self.REQUIRED_KEYS:
            if key not in self.attributes:
                return False
        return True

    def calculate(self):
        raise NotImplementedError


class CalculateStage(Calculate):
    """
    https://www.cancer.org/cancer/types/oral-cavity-and-oropharyngeal-cancer/detection-diagnosis-staging/staging.html
    """

    REQUIRED_KEYS = [
        S.PATHOLOGICAL_TNM,
    ]

    t: str
    n: str
    m: str

    def calculate(self):
        self.set_tnm()
        self.calculate_stage()

    def set_tnm(self):
        try:
            tnm = self.attributes[S.PATHOLOGICAL_TNM]
            tnm = tnm.replace('X', '0').replace('x', '0')  # x is unknown, should be treated as 0
            self.t = tnm.split('T')[1].split('N')[0]
            self.n = tnm.split('N')[1].split('M')[0]
            self.m = tnm.split('M')[1]
        except Exception as e:
            print(e)
            self.t, self.n, self.m = '', '', ''

    def calculate_stage(self):
        t, n, m = self.t, self.n, self.m
        if m == '1':
            stage = 'Stage IVC'
        elif t == '4b' and m == '0':
            stage = 'Stage IVB'
        elif n in ['3', '3a', '3b'] and m == '0':
            stage = 'Stage IVB'
        elif t in ['1', '2', '3', '4a'] and n in ['2', '2a', '2b', '2c'] and m == '0':
            stage = 'Stage IVA'
        elif t == '4a' and n in ['0', '1'] and m == '0':
            stage = 'Stage IVA'
        elif t in ['1', '2', '3'] and n == '1' and m == '0':
            stage = 'Stage III'
        elif t == '3' and n == '0' and m == '0':
            stage = 'Stage III'
        elif t == '2' and n == '0' and m == '0':
            stage = 'Stage II'
        elif t == '1' and n == '0' and m == '0':
            stage = 'Stage I'
        elif t == 'is' and n == '0' and m == '0':
            stage = 'Stage 0'
        else:
            print(f'WARNING! Invalid "{S.PATHOLOGICAL_TNM}": "{self.attributes[S.PATHOLOGICAL_TNM]}" for finding AJCC stage')
            stage = ''

        self.attributes[S.AJCC_STAGE] = stage
