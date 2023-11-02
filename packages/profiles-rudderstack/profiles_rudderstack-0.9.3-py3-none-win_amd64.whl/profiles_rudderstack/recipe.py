import hashlib
from inspect import getsource
from typing import Tuple
from abc import ABC, abstractmethod
from profiles_rudderstack.material import WhtMaterial

class PyNativeRecipe(ABC):
    @abstractmethod
    def prepare(self, this: WhtMaterial):
        """Prepare the material for execution. Add dependencies using de_ref, execute template, etc.
        
        Args:
            this (WhtMaterial): The material to be prepared
        """
        raise NotImplementedError()

    @abstractmethod
    def execute(self, this: WhtMaterial):
        """Execute the material

        Args:
            this (WhtMaterial): The material to be executed
        """
        raise NotImplementedError()
        
    @abstractmethod
    def describe(self, this: WhtMaterial) -> Tuple[str, str]:
        """Describe the material

        Args:
            this (WhtMaterial): The material to be described

        Returns:
            Tuple[str, str]: The content and extension of the material to be described
        """
        raise NotImplementedError()
    
    def hash(self):
        prepareCode = getsource(self.prepare)
        executeCode = getsource(self.execute)
        describeCode = getsource(self.describe)

        hash = hashlib.sha256()
        hash.update(prepareCode.encode('utf-8'))
        hash.update(executeCode.encode('utf-8'))
        hash.update(describeCode.encode('utf-8'))

        return hash.hexdigest()