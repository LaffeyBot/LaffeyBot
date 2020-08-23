define({ "api": [
  {
    "type": "post",
    "url": "/v1/record/add_record",
    "title": "出刀",
    "version": "1.0.0",
    "name": "add_record",
    "group": "Records",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "damage",
            "description": "<p>(必须)    伤害</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "boss_gen",
            "description": "<p>(必须)    boss周目</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "boss_order",
            "description": "<p>(必须)    第几个boss</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "回参": [
          {
            "group": "回参",
            "type": "String",
            "optional": false,
            "field": "msg",
            "description": "<p>为&quot;Successful!&quot;</p>"
          },
          {
            "group": "回参",
            "type": "Dictionary",
            "optional": false,
            "field": "data",
            "description": "<p>添加的Record，具体内容参照Record表</p>"
          }
        ]
      }
    },
    "error": {
      "examples": [
        {
          "title": "参数不存在",
          "content": "HTTP/1.1 400 Bad Request\n{\"msg\": \"Parameter is missing\", \"code\": 401}",
          "type": "json"
        },
        {
          "title": "用户没有加入公会",
          "content": "HTTP/1.1 403 Forbidden\n{\"msg\": \"User is not in any group.\", \"code\": 402}",
          "type": "json"
        },
        {
          "title": "用户的公会不存在",
          "content": "HTTP/1.1 403 Forbidden\n{\"msg\": \"User's group not found.\", \"code\": 403}",
          "type": "json"
        }
      ]
    },
    "filename": "server_app/record/record.py",
    "groupTitle": "Records"
  },
  {
    "type": "post",
    "url": "/v1/auth/login",
    "title": "登录",
    "version": "1.0.0",
    "name": "login",
    "group": "Users",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "username",
            "description": "<p>(可选)    用户名</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>(可选)    邮箱</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "phone",
            "description": "<p>(可选)    手机号</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>(必须)    密码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Request-Example:",
          "content": "{\n    username: \"someuser\",\n    password: \"12345678\"\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "回参": [
          {
            "group": "回参",
            "type": "String",
            "optional": false,
            "field": "msg",
            "description": "<p>为&quot;Successful!&quot;</p>"
          },
          {
            "group": "回参",
            "type": "String",
            "optional": false,
            "field": "jwt",
            "description": "<p>jwt token，应当放入auth header</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "成功样例",
          "content": "{ \"msg\": \"Successful!\",\n \"jwt\": \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c\"\n }",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "未提供用户名或密码",
          "content": "HTTP/1.1 403 Forbidden\n{\"msg\": \"Username or Password is missing\", \"code\": 201}",
          "type": "json"
        },
        {
          "title": "用户不存在",
          "content": "HTTP/1.1 403 Forbidden\n{\"msg\": \"User does not exist\", \"code\": 202}",
          "type": "json"
        },
        {
          "title": "密码或用户名错误",
          "content": "HTTP/1.1 403 Forbidden\n{\"msg\": \"Username or Password is incorrect\", \"code\": 203}",
          "type": "json"
        }
      ]
    },
    "filename": "server_app/auth/auth.py",
    "groupTitle": "Users"
  },
  {
    "type": "post",
    "url": "/v1/auth/sign_up",
    "title": "注册",
    "version": "1.0.0",
    "name": "sign_up",
    "group": "Users",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "username",
            "description": "<p>(必须)    用户名（3字以上）</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>(必须)    密码（8字以上）</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>(可选)    邮箱</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "phone",
            "description": "<p>(可选)    手机号</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Request-Example:",
          "content": "{\n    username: \"someuser\",\n    password: \"12345678\",\n    email: \"a@ddavid.net\",\n    phone: \"13312341234\"\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "回参": [
          {
            "group": "回参",
            "type": "String",
            "optional": false,
            "field": "msg",
            "description": "<p>为&quot;Successful!&quot;</p>"
          },
          {
            "group": "回参",
            "type": "String",
            "optional": false,
            "field": "id",
            "description": "<p>用户id</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "成功样例",
          "content": "HTTP/1.1 200 OK\n{\n    \"msg\": \"Successful!\",\n    \"id\": 12345\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "用户名或密码过短",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"msg\": \"Username or password is too short\",\n    \"code\": 102\n}",
          "type": "json"
        },
        {
          "title": "用户名已存在",
          "content": "HTTP/1.1 403 Forbidden\n{\"msg\": \"User Exists\", \"code\": 103}",
          "type": "json"
        }
      ]
    },
    "filename": "server_app/auth/auth.py",
    "groupTitle": "Users"
  }
] });
