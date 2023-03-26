create table imglite.user_index
(
    user_index    varchar(16) not null
        primary key,
    user_account  varchar(10) not null,
    user_password varchar(15) not null,
    user_uuid     char(32)    null,
    constraint user_index_pk
        unique (user_account, user_uuid)
);

create table imglite.img_type
(
    img_type      int auto_increment
        primary key,
    img_type_name char(3) not null,
    constraint img_type_pk
        unique (img_type_name)
);

create table imglite.img_index
(
    img_index       varchar(16)  not null
        primary key,
    img_name        varchar(127) not null,
    img_type        int          not null,
    img_uuid        char(32)     not null,
    img_upload_date date         not null,
    user_index      varchar(16)  not null,
    constraint img_index_pk
        unique (img_uuid),
    constraint img_index_img_type_null_fk
        foreign key (img_type) references imglite.img_type (img_type),
    constraint img_index_user_index_null_fk
        foreign key (user_index) references imglite.user_index (user_index)
);

create table imglite.invite_code
(
    invite_code varchar(5) not null
        primary key
);