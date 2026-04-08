
import argparse
from pathlib import Path
import traceback, sys






if __name__ == '__main__':
    # run as a program
    from lib.mdd_parser import parse
elif '.' in __name__:
    # package
    from .lib.mdd_parser import parse
else:
    # included with no parent package
    from lib.mdd_parser import parse





# import json, re
from datetime import datetime, timezone



def call_parse_program():
    config = {'arglist_strict':False}
    try:
        time_start = datetime.now()
        parser = argparse.ArgumentParser(
            description="Parse MDD Metadata",
            prog='mdmtoolsapram mdd_parse'
        )
        parser.add_argument(
            '-1',
            '--file',
            help='Input file',
            type=str,
            required=True
        )
        # parser.add_argument(
        #     '--config-something',
        #     help='Config: some config',
        #     type=str,
        #     choices = ["somethinga","somethingb"],
        #     required=False
        # )
        args = None
        args_rest = None
        if( ('arglist_strict' in config) and (not config['arglist_strict']) ):
            args, args_rest = parser.parse_known_args()
        else:
            args = parser.parse_args()
        inp_file = None
        if args.file:
            inp_file = Path(args.file)
            inp_file = '{inp_file}'.format(inp_file=inp_file.resolve())
        else:
            raise FileNotFoundError('Inp source: file not provided; please use --file')

        if not(Path(inp_file).is_file()):
            raise FileNotFoundError('file not found: {fname}'.format(fname=inp_file))


        config = {
        }
        # if args.config_something:
        #     config['xxx'] = yyy

        print('MDM parse script: script started at {dt}'.format(dt=time_start))

        with open(inp_file,'r',encoding='utf-8') as f:

            txt = f.read()

            result = parse(txt)

        time_finish = datetime.now()
        print('MDM parse script: finished at {dt} (elapsed {duration})'.format(dt=time_finish,duration=time_finish-time_start))
    except Exception as e:
        # for pretty-printing any issues that happened during runtime; if we hit FileNotFound I don't appreciate when a log traceback is shown, the error should be simple and clear
        # the program is designed to be user-friendly
        # that's why we reformat error messages a little bit
        # stack trace is still printed (I even made it longer to 20 steps!)
        # but the error message itself is separated and printed as the last message again

        # for example, I don't write 'print('File Not Found!');exit(1);', I just write 'raise FileNotFoundErro()'
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
