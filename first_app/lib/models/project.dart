import 'package:flutter/foundation.dart';

class CostComponent {
  String name;
  String? contractNumber;
  double? contractValue;
  double? disbursement;

  CostComponent({
    required this.name,
    this.contractNumber,
    this.contractValue,
    this.disbursement,
  });

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'contractNumber': contractNumber,
      'contractValue': contractValue,
      'disbursement': disbursement,
    };
  }

  factory CostComponent.fromJson(Map<String, dynamic> json) {
    return CostComponent(
      name: json['name'],
      contractNumber: json['contractNumber'],
      contractValue: json['contractValue'],
      disbursement: json['disbursement'],
    );
  }
}

class ConstructionProject {
  String name;
  double totalInvestment;
  List<CostComponent> costComponents;
  double capitalPlan;
  double totalDisbursement;

  ConstructionProject({
    required this.name,
    required this.totalInvestment,
    required this.costComponents,
    required this.capitalPlan,
    required this.totalDisbursement,
  });

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'totalInvestment': totalInvestment,
      'costComponents': costComponents.map((e) => e.toJson()).toList(),
      'capitalPlan': capitalPlan,
      'totalDisbursement': totalDisbursement,
    };
  }

  factory ConstructionProject.fromJson(Map<String, dynamic> json) {
    return ConstructionProject(
      name: json['name'],
      totalInvestment: json['totalInvestment'],
      costComponents: (json['costComponents'] as List)
          .map((e) => CostComponent.fromJson(e))
          .toList(),
      capitalPlan: json['capitalPlan'],
      totalDisbursement: json['totalDisbursement'],
    );
  }
}
