// Copyright 2021, the Flutter project authors. Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.

import 'course.dart';

class Assignment {
  final int id;
  final String title;
  final Course course;
  final bool isPopular;
  final bool isNew;

  Assignment(this.id, this.title, this.isPopular, this.isNew, this.course);
}