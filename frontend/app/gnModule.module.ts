import { NgModule } from "@angular/core";
import { CommonModule } from '@angular/common';
import { GN2CommonModule } from "@geonature_common/GN2Common.module";
import { Routes, RouterModule } from "@angular/router";
import { ProgramsComponent } from "./components/programs.component";
import { SitesComponent } from "./components/sites.component";

// my module routing
const routes: Routes = [
  { path: "", component: ProgramsComponent },
  { path: "sites/:id_program", component: SitesComponent }
];

@NgModule({
  declarations: [ProgramsComponent, SitesComponent],
  imports: [GN2CommonModule, RouterModule.forChild(routes), CommonModule],
  providers: [],
  bootstrap: []
})
export class GeonatureModule { }
