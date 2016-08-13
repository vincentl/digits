#include <stdlib.h>
#include <stdbool.h>

typedef struct dlx_t dlx_t;

typedef struct solution_t 
{
  size_t count;
  int    row[];
} solution_t;

void dlx_create(dlx_t **h);
void dlx_destroy(dlx_t *h);
void dlx_info(dlx_t *h, FILE *io);
void dlx_add_column(dlx_t *h, char *name, bool primary);
int  dlx_add_row(dlx_t *h, size_t count, int column[]);
void dlx_solve_by_recursion(dlx_t *h);

