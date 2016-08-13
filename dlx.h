#include <stdlib.h>
#include <stdbool.h>

typedef struct dlx_t dlx_t;

typedef struct solution_t 
{
  size_t count;
  int    row[];
} solution_t;

void dlx_create(dlx_t **x, size_t column_count);
void dlx_destroy(dlx_t *x);
void dlx_column_optional(dlx_t *x, size_t column_index);
void dlx_add_row(dlx_t *x, size_t count, int column[]);
int  dlx_solve(dlx_t *x, solution_t **solution);

