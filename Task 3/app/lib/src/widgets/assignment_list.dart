// Copyright 2021, the Flutter project authors. Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.

import 'package:flutter/material.dart';

import '../data.dart';

class AssignmentList extends StatelessWidget {
  final List<Assignment> assignments;
  final ValueChanged<Assignment>? onTap;

  const AssignmentList({
    required this.assignments,
    this.onTap,
    super.key,
  });

  @override
  Widget build(BuildContext context) => ListView.builder(
        itemCount: assignments.length,
        itemBuilder: (context, index) => ListTile(
          title: Text(
            assignments[index].title,
          ),
          subtitle: Text(
            assignments[index].course.name,
          ),
          onTap: onTap != null ? () => onTap!(assignments[index]) : null,
        ),
      );
}
