#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <capstone/capstone.h>
#include <sys/mman.h>

int upkeep() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
}

int validate(char* ptr, size_t len) {
    csh handle;
    cs_insn *insn;
    int ret = 1;

    if (cs_open(CS_ARCH_X86, CS_MODE_64, &handle) != CS_ERR_OK) {
        return 0;
    }
    size_t count = cs_disasm(handle, ptr, len, 0, 0, &insn);
    size_t success_len = 0;
    if (count > 0) {
        for (size_t j = 0; j < count; j++) {
            ret &= insn[j].mnemonic[0] == 'j';
            success_len += insn[j].size;
        }
        cs_free(insn, count);
    } else {
        return 0;
    }

    cs_close(&handle);

    ret &= len == success_len;
    return ret;
}


int main() {
    upkeep();

    char code[4096];
    size_t n = read(0, code, 0x1000);
    if (n > 0 && validate(code, n)) {
        ((void (*)())code)();
    } else {
        puts("That's not allowed! D:<");
    }
}
