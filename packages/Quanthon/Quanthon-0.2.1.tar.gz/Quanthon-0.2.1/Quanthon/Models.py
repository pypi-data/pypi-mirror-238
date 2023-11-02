# Under construction
import numpy as np

class Model():

    def __init__(self, integral_values, mapper='jw') -> None:
        '''
        args:
            integral_values: array of (*, 2) of integral values for the model.
        '''
        self.s = 'ad,a'
        
        mapper_dict = {'jw': self.jordan_wigner,
                       'other': self.other_mapper,
                       'special': self.special_mapper}
        
        self.states = np.zeros(np.log2(self.hamiltonian.shape[0]))

        if mapper not in self.mapper_dict.keys():
            self.mapper = mapper
        else:
            raise ValueError(f"Unknown mapper {mapper}.")
    
    def hamiltonian(self, pq_max):
        assert(type(pq_max) == int)
        range_of_pq = np.arange(0, pq_max)
        

    def adag(self, i):
        ''' applies the creation operator on state i.
        N.B. This state is the energy state of the model, not the quantum state used in quantum computers.'''
        
        if self.states[i] == 1:
            raise ValueError(f"State {i} is already occupied.")
        self.states[i] = 1


    def a(self,i):
        ''' applies the annihilation operator on state i'''

        if self.states[i] == 0:
            raise ValueError(f"Nothing to annihilate at state {i}.")
        self.states[i] = 0

    def jordan_wigner(self):

        return 
    
    def other_mapper(self):
        raise NotImplementedError('Other mappers are not implemented yet.')

        
    def _to_Pauli_strings(self, mapper='jw'):
        if self._special_mapping_exist:
            self._special_mapping()  
            
        pass

    def estimator(self):
        ''' Genrate the correct rotation to do the measurements for Hamilronians given by the pauli strings.
        
        return:
            (list) of the rotations 
        '''

        pass
        

class Lipkin(Model):

    def __init__(self, J) -> None:
        super().__init__()
        self._special_mapping_exist = True
        # self.hamiltonian = self._get_hamiltonian # some pre defined hamtiltonian
        
        if J > 0 and type(J) == int:
            self.J = J # the quasi-spin 
        else:
            raise ValueError('J must be a positive integer.')
        
    def _sepcial_mapping():
        pass
        
    def _get_hamiltonian(self, J):
        pass

    def estimator(self, qc, lmb, num_shots):
        '''Expectation value of the Hamiltonian'''
        return qc.expectation(self.Hamiltonian, lmb, num_shots)

class Ising(Model):

    def __init__(self, mapper='jw') -> None:
        super().__init__(mapper)


class Heisenberg(Model):

    def __init__(self, mapper='jw') -> None:
        super().__init__(mapper)
    
    
class SSH(Model):

    def __init__(self, mapper='jw') -> None:
        super().__init__(mapper)


class KitaevChain(Model):

    def __init__(self, mapper='jw') -> None:
        super().__init__(mapper)


