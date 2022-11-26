// Copyright 2021, the Flutter project authors. Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.

import 'package:flutter/material.dart';

import '../data.dart';

class CourseList extends StatelessWidget {
  final List<Course> courses;
  final ValueChanged<Course>? onTap;

  const CourseList({
    required this.courses,
    this.onTap,
    super.key,
  });

  @override
  Widget build(BuildContext context) => ListView.builder(
        itemCount: courses.length,
        itemBuilder: (context, index) => ListTile(
          title: Text(
            courses[index].name,
          ),
          subtitle: Text(
            '${courses[index].assignments.length} books',
          ),
          onTap: onTap != null ? () => onTap!(courses[index]) : null,
        ),
      );
}
