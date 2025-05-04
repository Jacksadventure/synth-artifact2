/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { Modal, Form, Table, Row, Col, Checkbox, Button, Alert } from 'antd';
import http from 'libs/http';
import envStore from '../environment/store';
import styles from './index.module.css';
import store from './store';