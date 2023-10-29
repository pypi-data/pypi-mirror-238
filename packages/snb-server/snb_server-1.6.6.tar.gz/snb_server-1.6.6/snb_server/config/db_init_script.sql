

insert into tb_snb_sys_image values('507b9df4d741-11ed25b2-32bf9c31-b6c3','Python3.8基础版','snb/node','v3',1,now(),now());
insert into tb_snb_sys_image values('507b9df4d741-11ed25b2-32bfc362-aa99','Python3.8机器学习版','snb/node','v3',1,now(),now());

insert into tb_snb_sys_machine_config values('507b9df4d741-11ed25b2-32bfc363-bf47','基本型','2000m','2048Mi','10Gi','',1,now(),now(),10);
insert into tb_snb_sys_machine_config values('507b9df4d741-11ed25b2-32bfc364-b7d0','增强型','4000m','4096Mi','20Gi','',1,now(),now(),20);


insert into tb_snb_user_invitation_code(status,create_time) values(-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now())
,(-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now())
,(-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now())
,(-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now())
,(-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now())
,(-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now())
,(-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now())
,(-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now())
,(-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now())
,(-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now()), (-2,now()),(-2,now())
;

select * from tb_snb_user_invitation_code;
update tb_snb_user_invitation_code set status=-1,code= concat(LPAD(id,2 , 0),floor(rand()*10),floor(rand()*10),floor(rand()*10),floor(rand()*10)) where status=-2;

select floor(rand()*10)