#include <stdio.h>
#include <limits.h>

#include "dlx.h"

typedef struct node_t node_t;

struct node_t
{
  node_t *L;
  node_t *R;
  node_t *U;
  node_t *D;
  int     S;
};

struct dlx_t
{
  size_t  column_count;
  node_t *h;
  node_t *column;
};

void dlx_create(dlx_t **_x, size_t column_count)
{
  size_t node_count = column_count + 1;
  dlx_t *x          = calloc(1, sizeof(dlx_t));
  x->h              = calloc(node_count, sizeof(node_t));
  x->column         = &x->h[1];
  x->column_count   = column_count;

  for( size_t i = 0; i <= column_count; ++i )
  {
    x->h[i].L = &x->h[(i - 1 + node_count) % node_count];
    x->h[i].R = &x->h[(i + 1) % node_count];
    x->h[i].U = &x->h[i];
    x->h[i].D = &x->h[i];
  }

  *_x = x;
}

void dlx_destroy(dlx_t *x)
{
  for( size_t i = 0; i < x->column_count; ++i )
    for( node_t *a = x->column[i].D, *n = x->column[i].D->D; a != &x->column[i]; a = n, n = n->D )
      free(a);

  free(x->h);
  free(x);
}

void dlx_column_optional(dlx_t *x, size_t column_index)
{
  x->column[column_index].S = INT_MIN; 
}

void dlx_add_row(dlx_t *x, size_t count, int column[])
{
  node_t *row[count];
  for( size_t i = 0; i < count; ++i )
  {
    node_t *v = calloc(1, sizeof(node_t));
    row[i]    = v;
    v->D      = &x->column[column[i]];
    v->U      = v->D->D;
    v->U->D   = v;
    v->D->U   = v;
    v->D->S  += 1;
  }

  for( size_t i = 0; i < count; ++i )
  {
    row[i]->R = row[(i+1) % count];
    row[i]->L = row[(i-1+count) % count];
  }
}

int  dlx_solve(dlx_t *x, solution_t **solution)
{
  for( node_t *a = x->h->R; a != x->h; a = a->R )
    printf( "column %d\n", a->S );
  return 0;
}


int main(int argc, char *argv[])
{
  dlx_t *x;
  dlx_create(&x, 3);
  dlx_column_optional(x, 2);

  int m[3][2] = {{1,0},{0,2},{0,0}};
  dlx_add_row(x, 1, m[0]);
  dlx_add_row(x, 2, m[1]);
  dlx_add_row(x, 1, m[2]);

  solution_t *s = NULL;
  
  while( dlx_solve(x, &s) )
  {
    printf( "solution with %zu rows:", s->count );
    for( size_t i = 0; i < s->count; ++i )
      printf( " %u", s->row[i] );
    printf( "\n" );
  }

  free(s);
  dlx_destroy(x);
  return 0;
}
