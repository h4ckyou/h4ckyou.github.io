void _init()
{
    if (__gmon_start__ != 0)
    {
        __gmon_start__();
    }
}

int64_t sub_1020()
{
    int64_t var_8 = 0;
    /* jump -> nullptr */
}

int64_t sub_1030()
{
    int64_t var_8 = 0;
    /* tailcall */
    return sub_1020();
}

int64_t sub_1040()
{
    int64_t var_8 = 1;
    /* tailcall */
    return sub_1020();
}

int64_t sub_1050()
{
    int64_t var_8 = 2;
    /* tailcall */
    return sub_1020();
}

int64_t sub_1060()
{
    int64_t var_8 = 3;
    /* tailcall */
    return sub_1020();
}

void __cxa_finalize(void* d)
{
    /* tailcall */
    return __cxa_finalize(d);
}

int32_t strncmp(char const* arg1, char const* arg2, uint64_t arg3)
{
    /* tailcall */
    return strncmp(arg1, arg2, arg3);
}

int32_t puts(char const* str)
{
    /* tailcall */
    return puts(str);
}

void __stack_chk_fail() __noreturn
{
    /* tailcall */
    return __stack_chk_fail();
}

char* fgets(char* buf, int32_t n, FILE* fp)
{
    /* tailcall */
    return fgets(buf, n, fp);
}

void _start(int64_t arg1, int64_t arg2, void (* arg3)()) __noreturn
{
    int64_t stack_end_1;
    int64_t stack_end = stack_end_1;
    __libc_start_main(main, __return_addr, &ubp_av, __libc_csu_init, __libc_csu_fini, arg3, &stack_end);
    /* no return */
}

void deregister_tm_clones()
{
    return;
}

void register_tm_clones()
{
    return;
}

void __do_global_dtors_aux()
{
    if (completed.8061 != 0)
    {
        return;
    }
    if (__cxa_finalize != 0)
    {
        __cxa_finalize(__dso_handle);
    }
    deregister_tm_clones();
    completed.8061 = 1;
}

void frame_dummy()
{
    /* tailcall */
    return register_tm_clones();
}

int32_t main(int32_t argc, char** argv, char** envp)
{
    void* fsbase;
    int64_t rax = *(fsbase + 0x28);
    int32_t var_44 = 0;
    void var_2f;
    void* var_40 = &var_2f;
    void buf;
    fgets(&buf, 0x1f, __TMC_END__);
    if (strncmp(&buf, "openECSC{", 9) == 0)
    {
        void* const var_50_1 = &data_1214;
        char var_1b;
        if (var_1b == 0x7d)
        {
            uint32_t rax_4 = *var_40;
            char var_45_4 = ((((0x83 + ((rax_4 << 4) + rax_4)) - (*(var_40 + 1) * 0x39)) + ((0 - *(var_40 + 5)) << 2)) + (*(var_40 + 0xa) * 0x7c));
            void* const var_50_2 = &data_1288;
            uint32_t rax_23 = *(var_40 + 0xf);
            if (((var_45_4 + (rax_23 - (rax_23 << 3))) + (*(var_40 + 0x13) * 0x3b)) == 0xf1)
            {
                uint32_t rax_35 = *(var_40 + 1);
                void* const var_50_3 = &data_130f;
                if ((((((0x6a + (*var_40 * 0x32)) + (((rax_35 << 3) + rax_35) * 2)) - (*(var_40 + 3) * 0x6b)) - (*(var_40 + 0xa) * 0x76)) - (*(var_40 + 0x13) * 0x27)) == 0x29)
                {
                    void* const var_50_4 = &data_137b;
                    uint32_t rax_66 = *(var_40 + 0xf);
                    char var_45_16 = (((((0xd0 - (*(var_40 + 3) * 0x51)) + (*(var_40 + 9) << 7)) + (*(var_40 + 0xd) * 0x67)) + ((rax_66 << 5) - rax_66)) + (*(var_40 + 0x12) * 0x24));
                    if (var_45_16 == 0xbb)
                    {
                        void* const var_50_5 = &data_13d7;
                        void* const var_50_6 = &data_13fc;
                        uint32_t rax_83 = *(var_40 + 3);
                        char var_45_20 = ((((0xb6 + ((0 - *var_40) << 6)) + ((rax_83 << 6) + rax_83)) + ((0 - *(var_40 + 5)) << 4)) - (*(var_40 + 7) * 0x66));
                        void* const var_50_7 = &data_1464;
                        void* const var_50_8 = &data_149b;
                        if (((((var_45_20 - (*(var_40 + 0xa) * 0x4e)) - (*(var_40 + 0xb) * 0x6b)) - (*(var_40 + 0xc) * 0x54)) == 0x5a && ((0xe9 + (*(var_40 + 3) * 0x78)) - (*(var_40 + 0x12) * 0x49)) == 0x3b))
                        {
                            void* const var_50_9 = &data_14ee;
                            void* const var_50_10 = &data_150f;
                            void* const var_50_11 = &data_1546;
                            char var_45_30 = (((((0x25 + (*(var_40 + 1) * 0x47)) - (*(var_40 + 5) * 0x45)) - (*(var_40 + 6) * 0x51)) + (*(var_40 + 7) * 0x28)) - (*(var_40 + 8) * 0x49));
                            void* const var_50_12 = &data_1581;
                            void* const var_50_13 = &data_15a6;
                            if ((((var_45_30 + (*(var_40 + 9) * 0x90)) - (*(var_40 + 0xb) * 0x52)) + *(var_40 + 0x11)) == 0x4c)
                            {
                                uint32_t rax_158 = *(var_40 + 3);
                                void* const var_50_14 = &data_160c;
                                void* const var_50_15 = &data_162d;
                                char var_45_38 = (((((0x92 - (*var_40 * 0x32)) + (rax_158 - (rax_158 << 4))) - (*(var_40 + 8) * 0x17)) - (*(var_40 + 0xb) * 0x19)) + ((0 - *(var_40 + 0xf)) << 6));
                                if (((var_45_38 - (*(var_40 + 0x10) * 0x44)) - (*(var_40 + 0x13) * 0x74)) == 0x32)
                                {
                                    void* const var_50_16 = &data_16a2;
                                    if (((((0x3d + (*(var_40 + 0xa) * 0x75)) + (*(var_40 + 0xd) * 0x2e)) + (*(var_40 + 0xf) * 0x43)) + (*(var_40 + 0x10) * 0x6b)) == 0x52)
                                    {
                                        void* const var_50_17 = &data_1713;
                                        if ((((5 + ((0 - *(var_40 + 7)) << 2)) + (*(var_40 + 0xb) * 0x71)) - (*(var_40 + 0x10) * 0x76)) == 8)
                                        {
                                            void* const var_50_18 = &data_1788;
                                            uint64_t rax_225 = (*(var_40 + 9) * 5);
                                            if ((((0xf1 + (*(var_40 + 2) * 0x65)) + ((0 - *(var_40 + 7)) << 6)) + (rax_225 + (rax_225 << 2))) == 0x84)
                                            {
                                                uint32_t rax_233 = *(var_40 + 5);
                                                void* const var_50_19 = &data_1808;
                                                void* const var_50_20 = &data_1824;
                                                void* const var_50_21 = &data_1845;
                                                char var_45_55 = (((((0x2d + (*(var_40 + 2) * 0x43)) + ((rax_233 << 7) - rax_233)) + (*(var_40 + 6) << 4)) + (*(var_40 + 0xa) * 0x27)) + -((*(var_40 + 0xb) * 5)));
                                                uint32_t rax_254 = *(var_40 + 0x10);
                                                if (((var_45_55 + ((rax_254 << 4) + rax_254)) + (*(var_40 + 0x13) * 0x2f)) == 0xd4)
                                                {
                                                    void* const var_50_22 = &data_18b6;
                                                    void* const var_50_23 = &data_18d7;
                                                    if (((0x25 - (*var_40 * 0x79)) - (*(var_40 + 0xd) * 0x22)) == 7)
                                                    {
                                                        void* const var_50_24 = &data_18ec;
                                                        void* const var_50_25 = &data_1911;
                                                        void* const var_50_26 = &data_192d;
                                                        char var_45_63 = ((((0x87 - (*(var_40 + 4) * 0x5b)) + (*(var_40 + 6) << 2)) - (*(var_40 + 0x11) * 0x67)) + ((0 - *(var_40 + 0x13)) << 2));
                                                        if (var_45_63 == 0x56)
                                                        {
                                                            void* const var_50_27 = &data_1972;
                                                            void* const var_50_28 = &data_1981;
                                                            void* const var_50_29 = &data_19a2;
                                                            uint32_t rax_296 = *(var_40 + 6);
                                                            void* const var_50_30 = &data_1a0e;
                                                            void* const var_50_31 = &data_1a3d;
                                                            uint32_t rax_322 = *(var_40 + 0x11);
                                                            void* const var_50_32 = &data_1a63;
                                                            char var_45_72 = (((((((((0x27 - (*(var_40 + 2) * 0x63)) + (*(var_40 + 5) * 0x61)) + ((rax_296 * 0xc) + rax_296)) + (*(var_40 + 0xa) * 0x14)) + (*(var_40 + 0xb) * 0x22)) + (*(var_40 + 0xd) * 0x17)) - *(var_40 + 0xe)) + ((((rax_322 << 2) + rax_322) * 2) + rax_322)) + (*(var_40 + 0x12) * 0x58));
                                                            void* const var_50_33 = &data_1a84;
                                                            if (var_45_72 == 0x11)
                                                            {
                                                                uint32_t rax_338 = *(var_40 + 8);
                                                                void* const var_50_34 = &data_1acc;
                                                                void* const var_50_35 = &data_1aed;
                                                                void* const var_50_36 = &data_1b0e;
                                                                char var_45_77 = (((((5 - (*(var_40 + 3) * 0x5a)) + (((rax_338 << 2) + rax_338) * 2)) - (*(var_40 + 0xc) * 0x75)) + (*(var_40 + 0x10) * 0x38)) - (*(var_40 + 0x12) * 0x23));
                                                                if (var_45_77 == 0x32)
                                                                {
                                                                    void* const var_50_37 = &data_1b6d;
                                                                    if (((0xc2 + (*(var_40 + 2) * 0xa0)) - (*(var_40 + 6) * 0x39)) == 4)
                                                                    {
                                                                        void* const var_50_38 = &data_1b86;
                                                                        uint32_t rax_368 = *(var_40 + 1);
                                                                        void* const var_50_39 = &data_1bbe;
                                                                        if ((((0xdf + (rax_368 - (rax_368 << 4))) + (*(var_40 + 0x11) * 0x53)) - (*(var_40 + 0x13) * 0x46)) == 0x5d)
                                                                        {
                                                                            void* const var_50_40 = &data_1be9;
                                                                            uint64_t rax_392 = (*(var_40 + 5) * 5);
                                                                            char var_45_87 = (((((0xf4 - (*(var_40 + 2) * 0x5d)) + (*(var_40 + 4) * 0x2b)) + (rax_392 + (rax_392 << 2))) - (*(var_40 + 7) * 0x26)) - (*(var_40 + 8) * 0x3d));
                                                                            void* const var_50_41 = &data_1c70;
                                                                            uint64_t rax_407 = (*(var_40 + 0xa) * 9);
                                                                            if ((var_45_87 + (rax_407 + (rax_407 << 3))) == 0x39)
                                                                            {
                                                                                void* const var_50_42 = &data_1ca5;
                                                                                if ((((0x37 + (*(var_40 + 0xe) * 0x62)) + (*(var_40 + 0x11) * 0x71)) + (*(var_40 + 0x12) * 0x58)) == 0xa3)
                                                                                {
                                                                                    void* const var_50_43 = &data_1d00;
                                                                                    void* const var_50_44 = &data_1d4d;
                                                                                    uint32_t rax_434 = *(var_40 + 0xb);
                                                                                    char var_45_96 = (((((0x40 - (*var_40 * 0xb)) - (*(var_40 + 1) * 0x64)) + (*(var_40 + 7) * 0x75)) + ((((rax_434 << 2) + rax_434) * 2) + rax_434)) - (*(var_40 + 0xf) * 0x4f));
                                                                                    void* const var_50_45 = &data_1d89;
                                                                                    if (var_45_96 == 0x19)
                                                                                    {
                                                                                        void* const var_50_46 = &data_1d9a;
                                                                                        var_44 = 1;
                                                                                    }
                                                                                }
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    char const* const str;
    if (var_44 == 0)
    {
        str = "Wrong!";
    }
    else
    {
        str = "Correct!";
    }
    puts(str);
    if (rax == *(fsbase + 0x28))
    {
        return 0;
    }
    __stack_chk_fail();
    /* no return */
}

void __libc_csu_init()
{
    _init();
    int64_t i = 0;
    do
    {
        int64_t rdx;
        int64_t rsi;
        int32_t rdi;
        &__frame_dummy_init_array_entry[i](rdi, rsi, rdx);
        i = (i + 1);
    } while (1 != i);
}

void __libc_csu_fini() __pure
{
    return;
}

int64_t _fini() __pure
{
    return;
}

