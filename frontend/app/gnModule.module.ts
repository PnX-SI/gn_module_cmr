import { NgModule } from "@angular/core";
import { CommonModule } from '@angular/common';
import { GN2CommonModule } from "@geonature_common/GN2Common.module";
import { Routes, RouterModule } from "@angular/router";
import { ProgramsComponent } from "./components/programs.component";
import { OperationsComponent } from "./components/operations.component";
import { IndividualsComponent } from "./components/form-individuals.component";


// my module routing
const routes: Routes = [
{ path: "", component: ProgramsComponent },
{ path: "operations", component: OperationsComponent },
{ path: "individuals", component: IndividualsComponent },
];

@NgModule({
  declarations: [ProgramsComponent, OperationsComponent, IndividualsComponent],
  imports: [GN2CommonModule, RouterModule.forChild(routes), CommonModule],
  providers: [],
  bootstrap: []
})
export class GeonatureModule { }
