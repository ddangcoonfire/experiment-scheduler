#TODO
 DDAN-15 딴다
 submitter 작업 브랜치를 불러온다 (git checkout [submitter-branch] submitter-file // git rebase [submitter-branch] )
 submitter_master.proto 정의 (example https://github.com/aimhubio/aim/blob/main/aim/ext/transport/proto/remote_tracking.proto)
 create automated code (example python -m grpc_tools.protoc -I experiment-scheduler/common/proto/master_task_manager.proto --python_out=. --grpc_python_out=. )
 create master inheriting grpc_server Master(grcp_server)
 submitter - master
 master - task manager
 common server class : grpc_server.py
 두 개의 상속받은 server class 필요. (master server, task manager server)
 목표 : submitter랑 통신이 된다
 태준 : request 작업이 왔을때 후처리
 수환 : request 가 되도록 grpc server 작업
 request data structure 는 submitter 명령어 기반 (ls, ps, run 등을 고려)