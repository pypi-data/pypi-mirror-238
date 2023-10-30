
import cli

def main():
    out = ' -o d:/mydocs/tmp/out.png'
    cmd = '--help'
    cmd = '-p source=sample/sample.scc'+out
    cmd = r'-cs MarsNI2001 -p source=D:\mydocs\tmp\test_opencratertools\test1.scc -p type=bpois,range=[8,20]' + out
    cmd = r'-pr cumul -cs neukumivanov -p source=sample\sample.binned'
    cmd = r'-legend n#r -cs marsni2001 -p source=D:\mydocs\tmp\test_opencratertools\test1.scc -p type=bpoiss,range=[6,80],offset_age=[14,-14]'
    cmd = r'-legend n#rap -cs marsni2001 -o D:\mydocs\data\congzhe\greg -p src="D:\mydocs\data\congzhe\greg\scarp1.scc" -p type=bp,range=[3,20]'
    cmd = r'-cs marsni2001 -p src=D:\mydocs\data\congzhe\greg\uplift.scc -p type=bpoi,range=[.6,1.2] -p range=[4,20]'

    
    print(f'\nDebugging command: craterstats '+cmd)
    a = cmd.split()
    cli.main(a)

if __name__ == '__main__':
    main()