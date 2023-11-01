from typing import Union,List,Tuple
from numbers import Number
from tabulate import tabulate


class Matrix():
    """
    This is only going to support passing a list or tuple of lists or tuples of numbers.
    ROW BASED ONLY.
    We're not going to write code to support passing columns.
    Also we're zero indexing. Get used to it.
    """
    def __init__(self,rows:Union[List,Tuple]=None):
        self.underlying=rows
        self.row_count=rows
        self.col_count=rows
        self.dimensions=None

    def __getitem__(self,index:list[int]): 
        """
        Allows user to directly index an entry from the underlying 2d list
        """           
        if isinstance(index,int):
            return self.underlying[index]
        if (len(index)==1 and isinstance(index[0],int)):
            return self.underlying[index[0]]
        if (len(index)==2 and isinstance(index[0],int) and isinstance(index[1],int)):
            return self.underlying[index[0]][index[1]]
        raise ValueError("keep indexes to 1 or 2 in length buddy-- and only integers!")

    def __setitem__(self,index:list[int],value):
        """
        Allows for directly setting an entry by its index        
        """
        if len(index)==2 and isinstance(index[0],int) and isinstance(index[1],int) and isinstance(value,Number):
            self.underlying[index[0]][index[1]]=value
        else:
            raise ValueError("Index must be length 2-- and only integers!")

    def __str__(self):
        """
        Pretty prints a matrix
        """
        return tabulate(self.underlying,tablefmt='grid')

    def __repr__(self):
        """
        Same as __str__
        """
        return self.__str__()

    def __eq__(self,other:'Matrix',accuracy:float=1/1000)->bool:
        """
        Compares matrices by size and entry-wise. For entry-wise comparison,
        defaults to comparing within .001 in order to account for floating point arithmetic
        """
        if not self.dimensions==other.dimensions:
            return False
        for i,row in enumerate(self.underlying):
            for j,entry in enumerate(row):
                if not self[i,j]-other[i,j] < accuracy:
                    return False
        return True

    @property
    def underlying(self):
        return self._underlying
    @underlying.setter
    def underlying(self,rows):
        if not isinstance(rows,Union[List,Tuple]):
            raise AttributeError("You must pass a tuple or list of floats.")
        _length_of_rows=len(rows[0])
        for item in rows:
            if not isinstance(item,Union[List,Tuple]):
                raise AttributeError("You must pass a tuple or list of floats!")
            if len(item)!=_length_of_rows:
                raise ValueError("You cannot pass a ragged array!")
            for entry in item:
                if not isinstance(entry,Number):
                    raise ValueError("We are only doing numerical Matrices.")
        self._underlying=rows

    @property
    def row_count(self):
        return self._row_count
    @row_count.setter
    def row_count(self,rows):
        self._row_count=len(rows)
    
    @property
    def col_count(self):
        return self._col_count
    @col_count.setter
    def col_count(self,rows):
        self._col_count=len(rows[0])

    @property
    def dimensions(self):
        return self._dimensions
    @dimensions.setter
    def dimensions(self,_):
        self._dimensions=(self.row_count,self.col_count)
    
    @classmethod
    def get_identity(cls,n:int=0)->'Matrix':
        """
        Returns an identity matrix with passed dimension.
        """
        if not (isinstance(n,int) and n > 0):
            raise ValueError("We want an integer > 0!")
        underlying=[[0,]*n for i in range(n)]
        for i,sub_list in enumerate(underlying):
            sub_list[i]=1
        return Matrix(underlying)

    @classmethod
    def swap_rows(cls,i:int=0,j:int=0,n:int=0)->'Matrix':
        """
        Returns the elementary matrix that swaps rows i and j.
        """
        if not (isinstance(n,int) and n > 0):
            raise ValueError("We want an integer > 0!")
        if not (isinstance(i,int) and (0<=i<n)):
            raise ValueError("i must be between 0 and n!")
        if not (isinstance(j,int) and (0<=i<n)):
            raise ValueError("i must be between 0 and n!")

        underlying=[[0,]*n for p in range(n)]
        for p,sub_list in enumerate(underlying):
            sub_list[p]=1

        underlying[i][i]=0
        underlying[i][j]=1
        underlying[j][j]=0
        underlying[j][i]=1
        return Matrix(underlying)
    
    @classmethod
    def rescale_row(cls,i:int=0,c:Number=0,n:int=0)->'Matrix':
        """
        Returns the Elementary matrix which scales row i by the numeric c when left multiplied.
        """
        if not (isinstance(n,int) and n > 0):
            raise ValueError("We want an integer > 0 for dimension!")
        if not (isinstance(i,int) and (0<=i<n)):
            raise ValueError("i must be between 0 and n!")

        underlying=[[0,]*n for p in range(n)]
        for p,sub_list in enumerate(underlying):
            sub_list[p]=1
        underlying[i][i]*=c
        return Matrix(underlying)

    @classmethod
    def add_ith_row_to_jth_row(cls,i:int=0,j:int=0,n:int=0)->'Matrix':
        """
        Returns elementary matrix to add the ith row to the jth row.
        """
        if not (isinstance(n,int) and n > 0):
            raise ValueError("We want an integer > 0 for dimension!")
        if not (isinstance(i,int) and (0<=i<n)):
            raise ValueError("i must be between 0 and n!")
        if not (isinstance(j,int) and (0<=j<n)):
            raise ValueError("j must be between 0 and n!")

        underlying=[[0,]*n for p in range(n)]
        for p,sub_list in enumerate(underlying):
            sub_list[p]=1
        underlying[j][i]=1
        return Matrix(underlying)

    @classmethod
    def m_mult(cls,matrices:list['Matrix']=[]):
        """
        Class method to implement matrix multiplication.
        """
        if not len(matrices)==2:
            raise ValueError("Let's keep this down to 1 product at a time, huh?")
        left_matrix=matrices[0]
        right_matrix=matrices[1]
        if not left_matrix.col_count == right_matrix.row_count:
            raise NotImplementedError(
                "This is an invalid operation: left matrix column count = %d, right matrix row count = %d" %
                (left_matrix.col_count,right_matrix.row_count)
                )
        result_underlying=[]
        #It's easier to implement row-wise, so we'll actually do our multiplication backwards!
        for row_index,row in enumerate(left_matrix.underlying):
            new_row=[]
            for col_index,_ in enumerate(range(right_matrix.col_count)):
                col=[x[col_index] for x in right_matrix.underlying]
                new_row.append(
                        sum(a*b for a,b in zip(row,col))
                )
            result_underlying.append(new_row)
        return Matrix(result_underlying)

    def get_row(self,n:int=0,as_matrix:bool=False)->list:
        """
        Returns the nth row of the matrix, assuming n < num_rows
        """
        if not (isinstance(n,int) and (0<=n<self.row_count)):
            raise ValueError("n must be an integer between 0 and %d" % self.row_count)
        if as_matrix:
            return Matrix([self.underlying[n]])
        return self.underlying[n]

    def get_col(self,n:int=0,as_matrix:bool=False)->list:
        """
        Returns the nth column of the matrix, assuming n < num_rows
        """
        if not (isinstance(n,int) and (0<=n<self.col_count)):
            raise ValueError("n must be an integer between 0 and %d" % self.col_count)
        if as_matrix:
            return Matrix([[x[n],] for x in self.underlying])
        return [x[n] for x in self.underlying]

    def is_identity(self)->bool:
        """
        Simple test to see if the matrix is an instance of the identity matrix for its dimensions.
        """
        if not self.is_square:
            return False
        for i,row in enumerate(self.underlying):
            for j,entry in enumerate(row):
                if i==j:
                    if entry != 1:
                        return False
                else:
                    if entry != 0:
                        return False
        return True

    def get_submatrix(self,n:int=0)->'Matrix':
        """
        returns the n x n submatrix of this matrix, starting at top left.
        """
        if n==0:
            raise ValueError("We don't do 0 dimensional Matrices.")
        max_possible=max(self.col_count,self.row_count)
        if n > max_possible:
            raise ValueError("This matrix doesn't support that.")
        return Matrix(
            [x[:n] for x in self.underlying[:n]]
        )

    def transpose(self)->'Matrix':
        """
        returns the transpose of this matrix.
        """
        return Matrix([self.get_col(i) for i in range(self.col_count)])

    def is_square(self)->bool:
        """
        checks to see whether or not this matrix is square.
        """
        return self.col_count==self.row_count

    def get_rank(self)->int:
        #this fails in some cases because it assumes we move pivots up when we have empty columns...we don't though
        rank=0
        test=self.get_elementary_decomposition(from_rank=True,track=False)[0]
        for i in range(min(self.dimensions)):
            if test[i,i]!=0:
                rank+=1
        if test.is_square():
            return rank
        else:
            if test.row_count<test.col_count:
                for k in range(i+1,test.col_count):
                    if test[i,k]!=0:
                        rank+=1
        return min(test.row_count,rank)


    def get_elementary_decomposition(self,track:bool=False,**kwargs):
        working_matrix=Matrix(self.underlying.copy())
        applied_matrices=[]
        small_dim=min(self.dimensions)
                
        for i in range(small_dim):
            #this block: if matrix[i,i]==0, go through the rest of the rows and try swapping them. If
            # matrix[i,i] still == 0 afterward, undo the swap and pretend it never happened.
            # If we never find a nonzero entry, we know the matrix is not invertible!
            _=i
            while working_matrix[i,i]==0:
                try:
                    _+=1
                    trial=Matrix.swap_rows(i,_,working_matrix.row_count)
                    working_matrix=Matrix.m_mult([trial,working_matrix])
                    if working_matrix[i,i]==0:
                        working_matrix=Matrix.m_mult([trial,working_matrix])
                    else:
                        applied_matrices.append(trial)
                except IndexError as e:
                    break
            del _
            if working_matrix[i,i]==0:
                continue#there are no nonzero entries in this column.
            if working_matrix[i,i] != 1:
                #scale row i to get it to 1.
                applied_matrices.append(Matrix.rescale_row(i,(1/working_matrix[i,i]),working_matrix.row_count))
                working_matrix=Matrix.m_mult([applied_matrices[-1],working_matrix])
                #we'll round the altered column to 3 decimal places for simplicity...
                for k in range(working_matrix.row_count):
                    working_matrix[i][k]=working_matrix[i][k]
            #at this point, w_m[i,i] should be 1.
            for j in range(i+1,working_matrix.row_count):
                #make the entries below matrix[i,i] zero by adding a scalar multiple of matrix[i].
                if working_matrix[j,i]!=0:
                    add_matrix=Matrix.add_ith_row_to_jth_row(i,j,working_matrix.row_count)
                    add_matrix[j,i]=-(working_matrix[j,i]/working_matrix[i,i])
                    applied_matrices.append(add_matrix)
                    working_matrix=Matrix.m_mult([applied_matrices[-1],working_matrix])
                    del add_matrix
        #here, we should be in R.E.F.
            for k in range(i):
                if working_matrix[k,i] != 0:
                    add_matrix=Matrix.add_ith_row_to_jth_row(j,k,working_matrix.row_count)
                    add_matrix[k,i]=-(working_matrix[k,i]/working_matrix[i,i])
                    applied_matrices.append(add_matrix)
                    working_matrix=Matrix.m_mult([applied_matrices[-1],working_matrix])
                    del add_matrix
        #we should now be in RREF.
        if not self.is_square():
            if not kwargs.get("from_rank"):
                raise NotImplementedError("This matrix is not square; it cannot be decomposed!")
            else:
                return [working_matrix]
        if track:#used for get_inverse function or if user wants to inspect the elementary matrices.
            return [working_matrix,applied_matrices]
        return [working_matrix]#this should be the most decomposed form we can get it to.
  
    def get_inverse(self)->'Matrix':
        if not self.is_square:
            raise NotImplementedError("Only a square matrix may be invertible.")
        if not self.get_rank()==self.col_count:
            raise NotImplementedError("This matrix is not invertible.")
        try:
            a=self.get_elementary_decomposition(track=True)[1]
            start=Matrix.get_identity(self.row_count)
            for i in a:
                start=Matrix.m_mult([i,start])
            for index,row in enumerate(start.underlying):
                for c_index,entry in enumerate(row):
                    if c_index!=index:
                        entry=round(entry,3)                    
            return start
        except Exception as e:
            raise NotImplementedError("This matrix MIGHT not be invertible... check the error manually") from e

