/*
 * The MIT License (MIT)
 * Copyright (c) 2016 Vincent Lucarelli
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
 * of the Software, and to permit persons to whom the Software is furnished to do
 * so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *
 */

#include <limits.h>
#include <regex.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct solution_t 
{
  size_t count;
  int    row[];
} solution_t;

typedef struct dlx_t dlx_t;

struct dlx_t
{
  dlx_t *L;
  dlx_t *R;
  dlx_t *U;
  dlx_t *D;
  dlx_t *C;
  int    S;
  int    I;
  char  *name;
};

void dlx_create(dlx_t **h);
void dlx_destroy(dlx_t *h);
void dlx_info(dlx_t *h, FILE *io);
void dlx_add_column(dlx_t *h, char *name, bool primary);
int  dlx_add_row(dlx_t *h, size_t count, int column[]);
void dlx_solve_by_recursion(dlx_t *h);

void dlx_create(dlx_t **_h)
{
  dlx_t *h = calloc(1, sizeof(dlx_t));
  
  h->U    = h->D = h;
  h->R    = h->L = h;
  h->I    = 0;
  h->S    = 0;
  h->name = NULL;
  
  *_h = h;
}

void dlx_info(dlx_t *h, FILE *io)
{
  fprintf(io, "%d x %d matrix\n", h->S, h->I);
  for( dlx_t *a = h->R; a != h; a = a->R )
    fprintf(io, " %ccolumn %3d/weight %4d : %s\n", a->S < 0 ? '-' : '+', a->I, a->S >0 ? a->S : -1, a->name ? a->name : "");
}

void dlx_destroy(dlx_t *h)
{
  for( dlx_t *A = h->R, *N = h->R->R; A != h; A = N, N = N->R )
  {
    for( dlx_t *a = A->D, *n = A->D->D; a != A; a = n, n = n->D )
    {
      free(a->name);
      free(a);
    }
    free(A->name);
    free(A);
  }
  free(h->name);
  free(h);
}

void dlx_add_column(dlx_t *h, char *name, bool primary)
{
  dlx_t *c = calloc(1,sizeof(dlx_t));
  
  c->U    = c->D = c;
  c->I    = h->I++;
  c->S    = primary ? 0 : INT_MIN;
  c->name = name ? strdup(name) : NULL;

  c->L    = h->L;
  c->R    = h;
  
  c->L->R = c;
  c->R->L = c;
}

int dlx_add_row(dlx_t *h, size_t count, int column[])
{
  dlx_t *row[count];

  for( size_t i = 0; i < count; ++i )
  {
    dlx_t *v = calloc(1, sizeof(dlx_t));
    row[i]   = v;
  
    dlx_t *c;
    for( c = h->R; c->I != column[i] && c != h; c = c->R );
    if( c->I != column[i] )
    {
      for( size_t j = 0; j <= i; ++j )
        free(row[j]);
      return 1;
    }
  
    v->C = c;
  }

  for( size_t i = 0; i < count; ++i )
  {
    dlx_t *v  = row[i];


    v->C->S  += 1;
    v->D      = v->C;
    v->U      = v->C->U;
    v->U->D   = v;
    v->D->U   = v;
    
    row[i]->R = row[(i+1) % count];
    row[i]->L = row[(i-1+count) % count];
  }

  h->S += 1;
  
  return 0;
}

void cover(dlx_t *c)
{
  c->R->L = c->L;
  c->L->R = c->R;

  for( dlx_t *i = c->D; i != c; i = i->D )
    for( dlx_t *j = i->R; j != i; j = j->R )
    {
      j->D->U  = j->U;
      j->U->D  = j->D;
      j->C->S -= 1;
    }
}

void uncover(dlx_t *c)
{
  for( dlx_t *i = c->U; i != c; i = i->U )
    for( dlx_t *j = i->L; j != i; j = j->L )
    {
      j->C->S += 1;
      j->D->U  = j;
      j->U->D  = j;
    }
  c->R->L = c;
  c->L->R = c;
}

void recurse(dlx_t *h, dlx_t **o, int k)
{
  // Scan for minimum weight, primary column
  dlx_t *c = NULL;
  int    T = INT_MAX;
  
  for( dlx_t *a = h->R; a != h; a = a->R )
  {
    if( a->S == 0 )
      return;

    if( a->S > 0 && a->S < T )
    {
      c = a;
      T = a->S;
    }
  }

  // If no primary column found, then have a solution
  if( c == NULL )
  {
    printf( "{\n" );

    for( int i = 0; i < k; ++i )
    {
      dlx_t *a = o[i];
      printf( "  '%s' : [", a->C->name);
      for( a = a->R; a != o[i]; a = a->R )
        printf( "%s,", a->C->name);
      printf( "],\n" );
    }
    printf( "},\n" );

    return;
  }

  // Recurse 
  cover(c);
  for( dlx_t *r = c->D; r != c; r = r->D )
  {
    o[k] = r;
    for( dlx_t *j = r->R; j != r; j = j->R )
      cover(j->C);
    recurse(h, o, k+1);
    r = o[k];
    c = r->C;
    for( dlx_t *j = r->L; j != r; j = j->L )
      uncover(j->C);
  }
  uncover(c);
}

void dlx_solve_by_recursion(dlx_t *h)
{
  size_t count = 0;
  for( dlx_t *c = h->R; c != h; c = c->R )
    count += c->S > 0 ? 1 : 0;
  
  dlx_t **o = calloc(count, sizeof(dlx_t *));
  recurse(h, o, 0);
  free(o);
}

void add_column(dlx_t *h, char *line, regmatch_t match[])
{
  bool primary = (line[match[3].rm_so] == '+');
  line[match[4].rm_eo] = '\0';
  dlx_add_column(h, &line[match[4].rm_so], primary);
}

int add_row(dlx_t *h, char *line, regmatch_t match[])
{
  line = &line[match[4].rm_so];
  if( line[0] != '[' )
    return 1;
  
  int    rc     = 0;
  size_t count  = 0;
  int   *column = NULL;
  char  *next   = NULL;

  for( line = &line[1]; line[0] != '\0'; line = &next[1] )
  {
    int value = strtoul(line, &next, 0);
    if( line == next )
    {
      rc = 1;
      break;
    }
 
    column          = realloc(column, (count+1)*sizeof(column[0]));
    column[count++] = value;
  }
  if( rc == 0 )
    rc = dlx_add_row(h, count, column); 
  
  free(column);
  return rc;
}

int parse_input(dlx_t *h, const char *path)
{
  FILE *io = fopen(path, "r");
  if(io == NULL)
  {
    fprintf(stderr, "failed to open '%s'\n", path);
    return 1;
  }

  regex_t    re;
  regmatch_t match[5];

  regcomp(&re, "^(column:)|^(matrix:)|^(\\+|-)[[:space:]]*(.+)", REG_EXTENDED);

  int     rc       = 0;
  char   *line     = NULL;
  size_t  capacity = 0;
  char    state    = '?';
  size_t  count    = 0;
  ssize_t length;
  
  while( (length = getline(&line, &capacity, io)) > 0 )
  {
    count           += 1;
    line[length - 1] = '\0';

    if(regexec(&re, line, sizeof(match)/sizeof(regmatch_t), match, 0))
    {
      rc++;
      fprintf(stderr, "skipping line %zu '%s'\n", count, line);
      continue;
    }
    
    int t;
    for( t = 1; t < sizeof(match)/sizeof(regmatch_t) && match[t].rm_so == -1; ++t );

    switch(t)
    {
      case  1: state = 'c'; fprintf(stderr, "found column start at line %zu\n", count); continue; break;
      case  2: state = 'm'; fprintf(stderr, "found matrix start at line %zu\n", count); continue; break;
      case  3: break;
      default: rc++; fprintf(stderr, "skipping line %zu '%s'\n", count, line); continue; break;
    }

    switch(state)
    {
      case '?': rc++; fprintf(stderr, "missing column/matrix ... skipping line %zu '%s'\n", count, line); continue; break;
      case 'c': add_column(h, line, match); break;
      case 'm': if(add_row(h, line, match) == 0) break;
      default : rc++; fprintf(stderr, "skipping line %zu '%s'\n", count, line); continue; break;
    }
  }

  free(line);
  regfree(&re);
  fclose(io);

  return rc;
}

int main(int argc, char *argv[])
{
  dlx_t *h = NULL;

  dlx_create(&h);
  int invalid = parse_input(h, argv[1]);
  if( invalid )
    fprintf( stderr, "**NOTE** skipped %d lines in %s\n", invalid, argv[1]);
  dlx_info(h, stderr);

  printf( "[\n" );
  dlx_solve_by_recursion(h);
  printf( "]\n" );

  dlx_destroy(h);

  return 0;
}
