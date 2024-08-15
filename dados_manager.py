
class DadosManager:
    def __init__(self):
        self.dados = {
            'bioma': None,
            'anos': None,
        }

    def set_bioma(self, bioma):
        self.dados['bioma'] = bioma

    def get_bioma(self):
        return self.dados['bioma']

    def set_anos(self, anos):
        self.dados['anos'] = anos

    def get_anos(self):
        return self.dados['anos']
