
import argparse
import traceback, sys






if __name__ == '__main__':
    # run as a program
    # from lib.mdd_parser import parse
    from program_parse_file import program_parse_file
elif '.' in __name__:
    # package
    # from .lib.mdd_parser import parse
    from .program_parse_file import program_parse_file
else:
    # included with no parent package
    # from lib.mdd_parser import parse
    from program_parse_file import program_parse_file








def call_parse_program():
    return program_parse_file({'arglist_strict':False})

def call_test_program():
    msg = '''
hello, world!
    '''
    print(msg)
    return True




run_programs = {
    'parse_mdd_metadata': call_parse_program,
    'test': call_test_program,
}



def main():
    try:
        parser = argparse.ArgumentParser(
            description="Universal caller of mdmtoolsap-py utilities"
        )
        parser.add_argument(
            #'-1',
            '--program',
            choices=dict.keys(run_programs),
            type=str,
            required=True
        )
        args, args_rest = parser.parse_known_args()
        if args.program:
            program = '{arg}'.format(arg=args.program)
            if program in run_programs:
                run_programs[program]()
            else:
                raise AttributeError('program to run not recognized: {program}'.format(program=args.program))
        else:
            print('program to run not specified')
            raise AttributeError('program to run not specified')
    except Exception as e:
        # the program is designed to be user-friendly
        # that's why we reformat error messages a little bit
        # stack trace is still printed (I even made it longer to 20 steps!)
        # but the error message itself is separated and printed as the last message again

        # for example, I don't write "print('File Not Found!');exit(1);", I just write "raise FileNotFoundErro()"
        print('',file=sys.stderr)
        print('Stack trace:',file=sys.stderr)
        print('',file=sys.stderr)
        traceback.print_exception(e,limit=20)
        print('',file=sys.stderr)
        print('',file=sys.stderr)
        print('',file=sys.stderr)
        print('Error:',file=sys.stderr)
        print('',file=sys.stderr)
        print('{e}'.format(e=e),file=sys.stderr)
        print('',file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()
