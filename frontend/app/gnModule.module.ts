import { NgModule } from "@angular/core";
import { CommonModule } from '@angular/common';
import { GN2CommonModule } from "@geonature_common/GN2Common.module";
import { Routes, RouterModule } from "@angular/router";
import { ProgramsListComponent } from "./components/programs.list.component";
import { ProgramsFormComponent } from "./components/programs.form.component";
import { OperationsComponent } from "./components/operations.component";
import { NomenclatureDisplayComponent } from "./utils/nomenclature_display.component";

// my module routing
const routes: Routes = [
  { path: "", component: ProgramsListComponent },
  { path: "form_pg", component: ProgramsFormComponent },
  { path: 'form_pg/:id', component: ProgramsFormComponent },
  { path: "operations", component: OperationsComponent },
  { path: "nomenclatures_display/:id_nomenclature", component: NomenclatureDisplayComponent },
];

@NgModule({
  declarations: [
    ProgramsListComponent, ProgramsFormComponent,
    OperationsComponent, NomenclatureDisplayComponent
  ],
  imports: [GN2CommonModule, RouterModule.forChild(routes), CommonModule],
  providers: [],
  bootstrap: []
})
export class GeonatureModule { }
