#include <stdio.h>

#define NUM_THREADS 1000000
#define ARRAY_SIZE 100
#define BLOCK_WIDTH 1000

//------------------------------------------------------------------------------

void print_array(int *array, int size) {
  printf("{ ");

  for (int i=0; i<size; i++) {
    printf("%d ", array[i]);
  }

  printf(" }");
}

//------------------------------------------------------------------------------

__global__ void increment_naive(int *g) {
  // determine thread
  int i = blockIdx.x * blockDim.x + threadIdx.x;

  // Wrap thread to array size
  i = i % ARRAY_SIZE;
  g[i] = g[i] + 1;
}

//------------------------------------------------------------------------------

__global__ void increment_atomic(int *g) {
  // determine thread
  int i = blockIdx.x * blockDim.x + threadIdx.x;

  // wrap thread to array size
  i = i % ARRAY_SIZE;
  atomicAdd(&g[i], 1);
}

//------------------------------------------------------------------------------

int main(int argc, char **argv) {
  printf("%d threads in %d blocks writing %d elements\n",
         NUM_THREADS,
         NUM_THREADS / BLOCK_WIDTH,
         ARRAY_SIZE);

  // array on host memory
  int h_array[ARRAY_SIZE];
  const int ARRAY_BYTES = ARRAY_SIZE * sizeof(int);

  // array on GPU
  int *d_array;
  cudaMalloc((void **) &d_array, ARRAY_BYTES);
  cudaMemset((void *) d_array, 0, ARRAY_BYTES);

  //increment_naive<<<NUM_THREADS/BLOCK_WIDTH, BLOCK_WIDTH>>>(d_array);
  increment_atomic<<<NUM_THREADS/BLOCK_WIDTH, BLOCK_WIDTH>>>(d_array);


  // copy results back from GPU
  cudaMemcpy(h_array, d_array, ARRAY_BYTES, cudaMemcpyDeviceToHost);

  print_array(h_array, ARRAY_SIZE);

  // free GPU memory
  cudaFree(d_array);

  return 0;

}
