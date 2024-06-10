undefined8 FUN_00101e97(char *key,char *param_2)

{
  undefined *puVar1;
  char cVar2;
  uint checksum;
  size_t sVar3;
  void *pvVar4;
  int fp;
  undefined8 ret;
  undefined *puVar5;
  long in_FS_OFFSET;
  int idx;
  int sub_idx;
  uint crc-idx;
  int o;
  int i;
  int j;
  int k;
  int l;
  int m;
  void *ptr;
  long local_a840;
  char *local_a838;
  int compute [6];
  uint array [10];
  uint matched [498];
  undefined local_a010 [40932];
  undefined2 delim;
  char generated [10];
  long canary;
  char *key_chunk;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  flag = "aa"
  cVar2 = regx_check(key);
  if (cVar2 != '\x01') {
    exit(1);
  }
  ptr = malloc(8);
  delim = 0x2d;
  if (ptr == (void *)0x0) {
    exit(1);
  }
  local_a840 = 0;
  local_a838 = strtok(key,(char *)&delim);
  while (local_a838 != (char *)0x0) {
    ptr = realloc(ptr,(local_a840 + 1) * 8);
    if (ptr == (void *)0x0) {
      exit(1);
    }
    sVar3 = strlen(local_a838);
    pvVar4 = malloc(sVar3 + 1);
    *(void **)(local_a840 * 8 + (long)ptr) = pvVar4;
    if (*(long *)((long)ptr + local_a840 * 8) == 0) {
                    /* WARNING: Subroutine does not return */
      exit(1);
    }
    key_chunk = *(char **)((long)ptr + local_a840 * 8);
    strcpy(key_chunk,local_a838);
    local_a840 = local_a840 + 1;
    local_a838 = strtok((char *)0x0,(char *)&delim);
  }
  array[0] = 1;
  array[1] = 0x37e;
  array[2] = 1;
  array[3] = 0x12a;
  array[4] = 0x1bf;
  array[5] = 0xc3204;
  array[6] = 1;
  array[7] = 0xdf;
  array[8] = 0xffffff4e;
  array[9] = 0xffffffff;
  memset(matched,0,0xa7a0);
  compute[0] = 0;
  compute[1] = 0;
  compute[2] = 0;
  compute[3] = 0;
  compute[4] = 0;
  compute[5] = 0;
  for (idx = 0; idx < 6; idx = idx + 1) {
    sub_idx = 0;
    for (crc-idx = array[(long)idx * 2]; (int)crc-idx <= (int)array[(long)idx * 2 + 1];
        crc-idx = crc-idx + 1) {
      checksum = gen_checksum(crc-idx ^ 0x37e);
      sprintf(generated,"%04X",(ulong)checksum);
      key_chunk = *(char **)((long)ptr + (long)idx * 8);
      fp = strcmp(generated,key_chunk);
      if (fp == 0) {
        matched[(long)idx * 0x6fc + (long)sub_idx] = crc-idx;
        sub_idx = sub_idx + 1;
      }
    }
    compute[idx] = sub_idx;
  }
  free(ptr);
  o = 0;
  do {
    if (compute[0] <= o) {
      printf("Incorrect Key Dear %s\n",param_2);
      fflush(1);
      ret = 0;
loop:
      if (canary == *(long *)(in_FS_OFFSET + 0x28)) {
        return ret;
      }
      __stack_chk_fail();
    }
    for (i = 0; i < compute[1]; i = i + 1) {
      for (j = 0; j < compute[2]; j = j + 1) {
        for (k = 0; k < compute[3]; k = k + 1) {
          for (l = 0; l < compute[4]; l = l + 1) {
            for (m = 0; m < compute[5]; m = m + 1) {
              if (((o * l + j == (m + i * i * i * i * i) - k) && (o + j < 0x6fc)) &&
                 (m - i * j < 0x37f)) {
                fp = strcmp(param_2,"BJIZ-HACKERLAB");
                if (fp == 0) {
                  printf("Correct key, Here the flag: %s\n",flag);
                  fflush(1);
                }
                else {
                  printf("Dear %s, WELCOME BACK\n",param_2);
                  fflush(1);
                }
                ret = 1;
                goto loop;
              }
            }
          }
        }
      }
    }
    o = o + 1;
  } while( true );
}
